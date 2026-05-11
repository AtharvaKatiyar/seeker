const GITHUB_URL = import.meta.env.VITE_GITHUB_URL

const GithubIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-3.5 h-3.5">
    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
  </svg>
)

const caveats = [
  "Thresholds are heuristic — may need tuning per machine or workload.",
  "Process termination is destructive — use Kill with care.",
  "Name-based grouping is practical but not perfect for all process models.",
  "Some processes may be inaccessible depending on system permissions.",
]

function Footer() {
  return (
    <footer className="bg-[#080808] border-t border-white/8 px-12 py-20 md:px-20">
      <div className="mx-auto max-w-6xl">

        {/* Caveats */}
        <div className="mb-16">
          <p className="mb-6 text-[11px] font-semibold tracking-[0.25em] uppercase text-white/25">
            Limitations
          </p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {caveats.map((c, i) => (
              <div key={i} className="flex items-start gap-4">
                <span className="mt-2 h-px w-4 flex-shrink-0 bg-white/15" />
                <p className="text-sm text-white/30 leading-relaxed">{c}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-white/8 pt-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <span className="text-sm font-black tracking-tight text-white/50">seeker</span>
            <span className="h-3 w-px bg-white/10" />
            <span className="text-[11px] tracking-[0.15em] uppercase text-white/20">
              memory sentinel
            </span>
          </div>

          <div className="flex items-center gap-6">
            <span className="text-[11px] text-white/15">Linux only</span>
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-[11px] tracking-[0.1em] uppercase text-white/25 hover:text-white/60 transition-colors"
            >
              <GithubIcon />
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
