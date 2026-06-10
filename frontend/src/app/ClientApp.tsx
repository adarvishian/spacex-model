import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import {
  decodeClientShare,
  downloadScenarioPackXlsx,
  downloadScenarioXlsx,
  fetchClientCalibrationStatus,
  fetchClientInputWhitelist,
  fetchClientScenarios,
  fetchHealth,
  runDeterministic,
} from "../api";
import { ModelProvenanceChip } from "../shared/ModelProvenanceChip";
import { CustomBuilder } from "../client/CustomBuilder";
import { DownloadsPanel } from "../client/DownloadsPanel";
import { HeadlinePanel } from "../client/HeadlinePanel";
import { ModuleSummaryGrid } from "../client/ModuleSummaryGrid";
import { ScenarioCards, type ScenarioChoice } from "../client/ScenarioCards";
import { MonteCarloPanel } from "../client/MonteCarloPanel";
import { ShareLinkButton } from "../client/ShareLinkButton";
import {
  defaultCustomValues,
  validateCustomValues,
  warningsFromApi,
} from "../shared/client-validation";
import { clientSummaryFromArtifact, clientSummaryFromDeterministic } from "../shared/client-precache";
import {
  getScenarioRunArtifact,
  isInstantPrecacheView,
  loadScenarioRunArtifact,
  preloadScenarioRunArtifacts,
} from "../shared/scenario-artifacts";
import { decodeShareState } from "../shared/share-link";
import type { ClientRunSummary } from "../shared/types";

function triggerDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function ClientApp() {
  const [searchParams] = useSearchParams();
  const [choice, setChoice] = useState<ScenarioChoice>("base_case");
  const [customValues, setCustomValues] = useState<Record<string, number>>({});
  const [run, setRun] = useState<ClientRunSummary | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [fieldWarnings, setFieldWarnings] = useState<Record<string, string>>({});
  const [artifactReady, setArtifactReady] = useState(false);

  const scenariosQ = useQuery({ queryKey: ["client-scenarios"], queryFn: fetchClientScenarios });
  const healthQ = useQuery({ queryKey: ["health"], queryFn: fetchHealth });
  const calibrationQ = useQuery({
    queryKey: ["client-calibration-status"],
    queryFn: fetchClientCalibrationStatus,
  });
  const inputsQ = useQuery({
    queryKey: ["client-whitelist"],
    queryFn: fetchClientInputWhitelist,
  });

  const inputs = inputsQ.data ?? [];
  const isServerless = Boolean(healthQ.data?.serverless);

  useEffect(() => {
    let cancelled = false;
    void preloadScenarioRunArtifacts()
      .then(() => {
        if (!cancelled) setArtifactReady(true);
      })
      .catch(() => {
        if (!cancelled) setArtifactReady(true);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (inputs.length && Object.keys(customValues).length === 0) {
      setCustomValues(defaultCustomValues(inputs));
    }
  }, [inputs, customValues]);

  const activeScenario = choice === "custom" ? "base_case" : choice;
  const activeOverrides = choice === "custom" ? customValues : {};

  const executeRun = useCallback(
    async (scenario: string, overrides: Record<string, number>) => {
      if (choice === "custom") {
        const { errors, warnings } = validateCustomValues(inputs, overrides);
        setFieldWarnings(warnings);
        if (Object.keys(errors).length) {
          setFieldErrors(errors);
          return false;
        }
        setFieldErrors({});
      } else {
        setFieldWarnings({});
      }

      if (Object.keys(overrides).length === 0 && isInstantPrecacheView(scenario, overrides)) {
        if (!artifactReady) {
          setRunning(true);
          setError(null);
          try {
            await loadScenarioRunArtifact(scenario);
          } finally {
            setRunning(false);
          }
        }
        const artifact = getScenarioRunArtifact(scenario);
        const summary = artifact ? clientSummaryFromArtifact(artifact) : null;
        if (summary) {
          setRun(summary);
          setError(null);
          return true;
        }
        if (isServerless) {
          setError(
            "Scenario data is not available offline. Regenerate precache artifacts or use Audit Mode.",
          );
          return false;
        }
      }

      if (isServerless && Object.keys(overrides).length > 0) {
        setError("Custom scenario runs require a live API key and are not available on this deployment yet.");
        return false;
      }

      setRunning(true);
      setError(null);
      try {
        const result = await runDeterministic({
          scenario,
          client_overrides: Object.keys(overrides).length ? overrides : undefined,
          use_cache: true,
        });
        setRun(clientSummaryFromDeterministic(result));
        setFieldWarnings(warningsFromApi(result.override_warnings));
        return true;
      } catch (e) {
        setError(String(e));
        return false;
      } finally {
        setRunning(false);
      }
    },
    [choice, inputs, artifactReady, isServerless],
  );

  useEffect(() => {
    const token = searchParams.get("s");
    if (!token || !inputs.length) return;
    let cancelled = false;
    (async () => {
      try {
        const decoded = await decodeClientShare(token).catch(() =>
          decodeShareState(token),
        );
        if (cancelled) return;
        setChoice("custom");
        setCustomValues({ ...defaultCustomValues(inputs), ...decoded.overrides });
        await executeRun(decoded.scenario, decoded.overrides);
      } catch (e) {
        if (!cancelled) setError(`Invalid share link: ${e}`);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [searchParams.get("s"), inputs.length]);

  useEffect(() => {
    if (searchParams.get("s")) return;
    if (choice === "custom") return;
    if (isInstantPrecacheView(choice, {}) && !artifactReady) return;
    void executeRun(choice, {});
  }, [choice, artifactReady, searchParams.get("s")]);

  const onCustomChange = (id: string, value: number) => {
    const next = { ...customValues, [id]: value };
    setCustomValues(next);
    if (choice === "custom" && inputs.length) {
      const { errors, warnings } = validateCustomValues(inputs, next);
      setFieldErrors(errors);
      setFieldWarnings(warnings);
    }
  };

  const onCustomRun = () => {
    void executeRun("base_case", customValues);
  };

  const onResetCustom = () => {
    setCustomValues(defaultCustomValues(inputs));
    setFieldErrors({});
    setFieldWarnings({});
  };

  const publicBaseUrl = useMemo(() => window.location.origin, []);

  const onDownloadActive = async () => {
    if (!run) return;
    setDownloading("active");
    try {
      const blob = await downloadScenarioXlsx({
        run_id: run.run_id,
        scenario: activeScenario,
        overrides: activeOverrides,
        public_base_url: publicBaseUrl,
      });
      triggerDownload(blob, `spacex_${activeScenario}.xlsx`);
    } catch (e) {
      setError(String(e));
    } finally {
      setDownloading(null);
    }
  };

  const onDownloadPack = async () => {
    setDownloading("pack");
    try {
      const blob = await downloadScenarioPackXlsx(publicBaseUrl);
      triggerDownload(blob, "spacex_scenario_pack.xlsx");
    } catch (e) {
      setError(String(e));
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="client-app" data-testid="client-app">
      <header className="audit-header client-header">
        <div className="audit-header-left">
          <h1>Mach33 · SpaceX Valuation</h1>
          <span className="audit-badge">CLIENT MODE</span>
        </div>
        <div className="audit-header-meta">
          <ModelProvenanceChip
            mode="client"
            workbookName={healthQ.data?.workbook_name}
            workbookMtime={healthQ.data?.workbook_mtime}
          />
          <Link to="/audit/starlink" className="mode-switch">
            Switch to Audit →
          </Link>
        </div>
      </header>

      <main className="client-main">
        {calibrationQ.data && !calibrationQ.data.calibrated && (
          <div className="audit-alert warning" data-testid="uncalibrated-banner">
            Model calibration in progress — {calibrationQ.data.pending_count} of{" "}
            {calibrationQ.data.total_count} S-1 disclosure anchors pending. Outputs are
            work-in-progress, not audit-grade.
          </div>
        )}
        {error && <div className="audit-alert error">{error}</div>}

        <ScenarioCards
          cards={scenariosQ.data ?? []}
          selected={choice}
          onSelect={(id) => {
            setChoice(id);
            setError(null);
          }}
        />

        <div className="client-content-grid">
          <div className="client-column-primary">
            <HeadlinePanel run={run} loading={running} />
            <MonteCarloPanel scenario={activeScenario} overrides={activeOverrides} />
            <ModuleSummaryGrid run={run} />
          </div>
          <div className="client-column-secondary">
            <CustomBuilder
              inputs={inputs}
              values={customValues}
              onChange={onCustomChange}
              fieldErrors={fieldErrors}
              fieldWarnings={fieldWarnings}
              onRun={onCustomRun}
              onReset={onResetCustom}
              running={running}
              visible={choice === "custom"}
            />
            <DownloadsPanel
              onDownloadActive={onDownloadActive}
              onDownloadPack={onDownloadPack}
              downloading={downloading}
              disabled={!run}
            />
            {choice === "custom" && (
              <ShareLinkButton
                scenario="base_case"
                overrides={customValues}
                disabled={Object.keys(fieldErrors).length > 0}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
