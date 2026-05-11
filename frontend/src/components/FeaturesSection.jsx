const features = [
  {
    index: "01",
    title: "Continuous Sampling",
    description:
      "Polls system RAM and per-process RSS every second. Tracks total, available, used memory and percent — always current, never stale.",
  },
  {
    index: "02",
    title: "State Analysis Engine",
    description:
      "Classifies system state as NORMAL, WARNING, or DANGER based on thresholds. Detects rapid memory growth and emits SPIKE events automatically.",
  },
  {
    index: "03",
    title: "Process Intelligence",
    description:
      "Groups processes by name to show true application footprint. Identifies newly spawned heavy processes and tracks top offenders in real time.",
  },
  {
    index: "04",
    title: "Smart Cooldowns",
    description:
      "Events are rate-limited with a 5-second cooldown window per event type. No alert spam — only meaningful, actionable notifications surface.",
  },
  {
    index: "05",
    title: "Direct Intervention",
    description:
      "Kill or Ignore any process directly from the floating UI. Under DANGER conditions, seeker can auto-terminate high-impact non-safe processes.",
  },
  {
    index: "06",
    title: "Always-on-top UI",
    description:
      "Frameless, translucent floating widget that stays above all windows. Drag it anywhere, expand cards for history, collapse when not needed.",
  },
]

function FeaturesSection() {
  return (
    <section className="bg-[#080808] px-12 py-28 md:px-20">
      <div className="mx-auto max-w-6xl">

        {/* Section label */}
        <div className="mb-16 flex items-center gap-6">
          <span className="text-[11px] font-semibold tracking-[0.25em] uppercase text-white/25">
            Capabilities
          </span>
          <span className="h-px flex-1 bg-white/8" />
        </div>

        {/* Headline */}
        <h2 className="mb-20 text-[clamp(2rem,5vw,3.5rem)] font-black leading-tight tracking-tight text-white">
          Observation.<br />Interpretation.<br />Action.
        </h2>

        {/* Feature list — ruled rows, no boxes */}
        <div>
          {features.map((f, i) => (
            <div
              key={f.index}
              className="group grid grid-cols-[3rem_1fr_2fr] items-start gap-8 border-t border-white/8 py-8 last:border-b transition-colors hover:border-white/15"
            >
              <span className="text-[11px] font-mono text-white/20 pt-0.5">
                {f.index}
              </span>
              <h3 className="text-sm font-semibold tracking-wide text-white/70 group-hover:text-white transition-colors">
                {f.title}
              </h3>
              <p className="text-sm leading-relaxed text-white/35 group-hover:text-white/50 transition-colors">
                {f.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default FeaturesSection
