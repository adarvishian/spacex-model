import { methodologyDownloadUrl } from "../api";

type Props = {
  onDownloadActive: () => void;
  onDownloadPack: () => void;
  downloading: string | null;
  disabled?: boolean;
};

export function DownloadsPanel({
  onDownloadActive,
  onDownloadPack,
  downloading,
  disabled,
}: Props) {
  return (
    <section className="client-downloads panel" aria-label="Downloads">
      <h2>Downloads</h2>
      <ul className="client-download-list">
        <li>
          <button
            type="button"
            className="client-download-btn"
            onClick={onDownloadActive}
            disabled={disabled || downloading !== null}
          >
            {downloading === "active" ? "Generating…" : "Active scenario (.xlsx)"}
          </button>
        </li>
        <li>
          <button
            type="button"
            className="client-download-btn"
            onClick={onDownloadPack}
            disabled={downloading !== null}
          >
            {downloading === "pack" ? "Generating…" : "Scenario pack — Base + Bear + Bull (.xlsx)"}
          </button>
        </li>
        <li>
          <a
            className="client-download-btn"
            href={methodologyDownloadUrl()}
            download="mach33_methodology_one_pager.txt"
          >
            Methodology one-pager (.txt)
          </a>
        </li>
      </ul>
    </section>
  );
}
