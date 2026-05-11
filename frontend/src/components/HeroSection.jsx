import { InteractiveGridPattern } from "./ui/interactive-grid-pattern"

const GITHUB_URL = import.meta.env.VITE_GITHUB_URL

const GithubIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
  </svg>
)

function Hero() {
  return (
    <div className="relative h-screen w-full overflow-hidden bg-[#080808]">
      {/* Full-screen interactive grid */}
      <InteractiveGridPattern cellSize={48} />

      {/* Subtle vignette so center text pops */}
      <div className="pointer-events-none absolute inset-0 bg-radial-[ellipse_60%_50%_at_50%_50%] from-transparent to-[#080808]/80" />

      {/* Content — left-aligned, Swiss grid */}
      <div className="relative z-10 flex h-full flex-col justify-end px-12 pb-20 md:px-20 md:pb-24">

        {/* Top-left label */}
        <div className="absolute top-10 left-12 md:left-20 flex items-center gap-6">
          <span className="text-[11px] font-semibold tracking-[0.2em] uppercase text-white/30">
            seeker
          </span>
          <span className="h-px w-8 bg-white/10" />
          <span className="text-[11px] tracking-[0.15em] uppercase text-white/20">
            v0.1.0 (Pre-release)
          </span>
        </div>

        {/* Top-right links */}
        <div className="absolute top-10 right-12 md:right-20 flex items-center gap-6">
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-[11px] tracking-[0.15em] uppercase text-white/30 hover:text-white/70 transition-colors"
          >
            <GithubIcon />
            GitHub
          </a>
        </div>

        {/* Main headline */}
        <div className="mb-10">
          <p className="mb-5 text-[11px] font-semibold tracking-[0.25em] uppercase text-white/30">
            Linux · Real-time · Lightweight
          </p>
          <h1 className="text-[clamp(4rem,12vw,10rem)] font-black leading-[0.9] tracking-tight text-white">
            seeker
          </h1>
          <p className="mt-4 text-[clamp(1rem,2vw,1.25rem)] font-light tracking-[0.3em] uppercase text-white/40">
            memory sentinel
          </p>
        </div>

        {/* Divider */}
        <div className="mb-8 h-px w-full bg-white/10" />

        {/* Bottom row */}
        <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
          <p className="max-w-md text-sm leading-relaxed text-white/40">
            Watches system RAM behavior, detects risky patterns, and surfaces
            actionable alerts through a lightweight floating UI. Answers one
            question: what is hurting your system right now?
          </p>

          <a
            href="https://github.com/AtharvaKatiyar/seeker/releases/download/v0.1.0/seeker"
            download="seeker"
            className="group inline-flex items-center gap-3 self-start sm:self-auto"
          >
            <span className="text-sm font-semibold tracking-[0.1em] uppercase text-white transition-colors group-hover:text-white/60">
              Download Binary
            </span>
            <span className="flex h-8 w-8 items-center justify-center border border-white/20 transition-all group-hover:border-white/50 group-hover:bg-white/5">
              <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-3.5 h-3.5 text-white/60">
                <path d="M8 2v9M4 8l4 4 4-4" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </span>
          </a>
        </div>
      </div>
    </div>
  )
}

export default Hero
