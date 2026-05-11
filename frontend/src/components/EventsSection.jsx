const events = [
  {
    type: "SPIKE",
    color: "text-amber-400/80",
    description:
      "A process or system memory jumped by more than 1 GB in a single sampling cycle.",
  },
  {
    type: "WARNING",
    color: "text-red-400/80",
    description:
      "RAM usage exceeded 80%. The top offending process is highlighted for action.",
  },
  {
    type: "NEW_HEAVY",
    color: "text-sky-400/80",
    description:
      "A newly started process immediately consumed over 1 GB of RAM.",
  },
  {
    type: "PRESSURE_CHANGE",
    color: "text-violet-400/80",
    description:
      "Pressure level crossed a range boundary: NORMAL → ELEVATED → HIGH → CRITICAL.",
  },
  {
    type: "AUTO_KILL",
    color: "text-white/40",
    description:
      "Under DANGER conditions, seeker terminated a high-impact non-safe process automatically.",
  },
]

const pressureLevels = [
  { label: "NORMAL",   range: "< 60%",  pct: 28,  color: "bg-white/20" },
  { label: "ELEVATED", range: "> 60%",  pct: 55,  color: "bg-white/35" },
  { label: "HIGH",     range: "> 75%",  pct: 72,  color: "bg-white/55" },
  { label: "CRITICAL", range: "> 85%",  pct: 90,  color: "bg-white/80" },
]

function EventsSection() {
  return (
    <section className="bg-[#080808] border-t border-white/8 px-12 py-28 md:px-20">
      <div className="mx-auto max-w-6xl">

        {/* Section label */}
        <div className="mb-16 flex items-center gap-6">
          <span className="text-[11px] font-semibold tracking-[0.25em] uppercase text-white/25">
            Event types
          </span>
          <span className="h-px flex-1 bg-white/8" />
        </div>

        <div className="grid grid-cols-1 gap-20 lg:grid-cols-2">

          {/* Left — event list */}
          <div>
            <h2 className="mb-12 text-[clamp(1.75rem,4vw,2.75rem)] font-black leading-tight tracking-tight text-white">
              What seeker detects
            </h2>

            <div>
              {events.map((e) => (
                <div
                  key={e.type}
                  className="group grid grid-cols-[7rem_1fr] gap-6 border-t border-white/8 py-6 last:border-b hover:border-white/15 transition-colors"
                >
                  <span className={`text-[11px] font-bold tracking-[0.15em] uppercase pt-0.5 ${e.color}`}>
                    {e.type}
                  </span>
                  <p className="text-sm leading-relaxed text-white/35 group-hover:text-white/50 transition-colors">
                    {e.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Right — pressure levels */}
          <div className="flex flex-col justify-center">
            <h3 className="mb-10 text-xs font-semibold tracking-[0.2em] uppercase text-white/25">
              Memory pressure scale
            </h3>

            <div className="space-y-8">
              {pressureLevels.map((p) => (
                <div key={p.label}>
                  <div className="mb-2 flex items-baseline justify-between">
                    <span className="text-[11px] font-bold tracking-[0.2em] uppercase text-white/50">
                      {p.label}
                    </span>
                    <span className="text-[11px] font-mono text-white/20">{p.range}</span>
                  </div>
                  <div className="h-px w-full bg-white/8">
                    <div
                      className={`h-px ${p.color} transition-all`}
                      style={{ width: `${p.pct}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <p className="mt-12 text-xs leading-relaxed text-white/20">
              Thresholds are heuristic and may need tuning per machine or workload.
              Safe process names are protected by default and will never be auto-killed.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default EventsSection
