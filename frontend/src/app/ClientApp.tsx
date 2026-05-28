import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import {
  decodeClientShare,
  downloadScenarioPackXlsx,
  downloadScenarioXlsx,
  fetchClientInputWhitelist,
  fetchClientScenarios,
  runDeterministic,
} from "../api";
import type { DeterministicRun } from "../api";
import { CustomBuilder } from "../client/CustomBuilder";
import { DownloadsPanel } from "../client/DownloadsPanel";
import { HeadlinePanel } from "../client/HeadlinePanel";
import { ModuleSummaryGrid } from "../client/ModuleSummaryGrid";
import { ScenarioCards, type ScenarioChoice } from "../client/ScenarioCards";
import { ShareLinkButton } from "../client/ShareLinkButton";
import {
  defaultCustomValues,
  validateCustomValues,
  warningsFromApi,
} from "../shared/client-validation";
import { decodeShareState } from "../shared/share-link";
import type { ClientRunSummary } from "../shared/types";

function toClientSummary(run: DeterministicRun): ClientRunSummary {
  const groupFcf = run.group?.group_fcf;
  return {
    run_id: run.run_id,
    scenario: run.scenario,
    valuation: run.valuation,
    module_ev: run.module_ev,
    group: {
      group_fcf: {
        years: groupFcf?.years ?? [],
        values: groupFcf?.values ?? [],
      },
    },
    modules: run.modules as ClientRunSummary["modules"],
    override_warnings: run.override_warnings,
  };
}

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

  const scenariosQ = useQuery({ queryKey: ["client-scenarios"], queryFn: fetchClientScenarios });
  const inputsQ = useQuery({
    queryKey: ["client-whitelist"],
    queryFn: fetchClientInputWhitelist,
  });

  const inputs = inputsQ.data ?? [];

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
        const { errors } = validateCustomValues(inputs, overrides);
        if (Object.keys(errors).length) {
          setFieldErrors(errors);
          return false;
        }
      }
      setRunning(true);
      setError(null);
      setFieldErrors({});
      try {
        const result = await runDeterministic({
          scenario,
          client_overrides: Object.keys(overrides).length ? overrides : undefined,
          use_cache: true,
        });
        setRun(toClientSummary(result));
        setFieldWarnings(warningsFromApi(result.override_warnings));
        return true;
      } catch (e) {
        setError(String(e));
        return false;
      } finally {
        setRunning(false);
      }
    },
    [choice, inputs],
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
    if (choice !== "custom") {
      void executeRun(choice, {});
    }
  }, [choice]);

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
    <div className="client-app">
      <header className="audit-header client-header">
        <div className="audit-header-left">
          <h1>Mach33 · SpaceX Valuation</h1>
          <span className="audit-badge">CLIENT MODE</span>
        </div>
        <Link to="/audit/starlink" className="mode-switch">
          Switch to Audit →
        </Link>
      </header>

      <main className="client-main">
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
            <ModuleSummaryGrid run={run} />
          </div>
          <div className="client-column-secondary">
            <CustomBuilder
              inputs={inputs}
              values={customValues}
              onChange={(id, v) =>
                setCustomValues((prev) => ({ ...prev, [id]: v }))
              }
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
