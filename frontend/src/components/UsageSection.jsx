const controls = [
  { gesture: "Drag header",        description: "Move the floating window anywhere on screen" },
  { gesture: "Double-click card",  description: "Expand or collapse the event log history for that process" },
  { gesture: "Ignore",             description: "Suppress alerts for that process key for 10 seconds" },
  { gesture: "Kill",               description: "Terminate all matching process instances immediately" },
]

const structure = [
  {
    file: "main.py",
    desc: "Entry point. Starts core monitoring in a background thread, launches PyQt6 UI in the main thread.",
  },
  {
    file: "core.py",
    desc: "Data collection, analysis rules, process grouping, event detection, pressure tracking, auto-kill logic.",
  },
  {
    file: "ui.py",
    desc: "Floating event-card interface. Handles Kill, Ignore, lifecycle cleanup, and event rendering.",
  },
]

const principles = [
  { num: "01", title: "Fast feedback",   desc: "Near real-time updates with a 1-second sampling loop." },
  { num: "02", title: "Low friction",    desc: "Always-on-top, compact, frameless UI that stays out of your way." },
  { num: "03", title: "Actionability",   desc: "Every critical alert can lead to an immediate response." },
]

function UsageSection() {
  return (
    <section className="bg-[#080808] border-t border-white/8 px-12 py-28 md:px-20">
      <div className="mx-auto max-w-6xl space-y-28">

        {/* Controls + Architecture */}
        <div className="grid grid-cols-1 gap-20 lg:grid-cols-2">

          {/* Controls */}
          <div>
            <div className="mb-12 flex items-center gap-6">
              <span className="text-[11px] font-semibold tracking-[0.25em] uppercase text-white/25">
                UI Controls
              </span>
              <span className="h-px flex-1 bg-white/8" />
            </div>

            <div>
              {controls.map((c) => (
                <div
                  key={c.gesture}
                  className="group grid grid-cols-[8rem_1fr] gap-6 border-t border-white/8 py-5 last:border-b hover:border-white/15 transition-colors"
                >
                  <span className="text-[11px] font-mono text-white/35 pt-0.5 group-hover:text-white/55 transition-colors">
                    {c.gesture}
                  </span>
                  <p className="text-sm text-white/35 leading-relaxed group-hover:text-white/50 transition-colors">
                    {c.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Architecture */}
          <div>
            <div className="mb-12 flex items-center gap-6">
              <span className="text-[11px] font-semibold tracking-[0.25em] uppercase text-white/25">
                Architecture
              </span>
              <span className="h-px flex-1 bg-white/8" />
            </div>

            <div>
              {structure.map((s) => (
                <div
                  key={s.file}
                  className="group border-t border-white/8 py-5 last:border-b hover:border-white/15 transition-colors"
                >
                  <span className="mb-1.5 block text-xs font-bold font-mono text-white/50 group-hover:text-white/70 transition-colors">
                    {s.file}
                  </span>
                  <p className="text-sm text-white/30 leading-relaxed group-hover:text-white/45 transition-colors">
                    {s.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Design principles */}
        <div>
          <div className="mb-16 flex items-center gap-6">
            <span className="text-[11px] font-semibold tracking-[0.25em] uppercase text-white/25">
              Design philosophy
            </span>
            <span className="h-px flex-1 bg-white/8" />
          </div>

          <div className="grid grid-cols-1 gap-0 sm:grid-cols-3">
            {principles.map((p, i) => (
              <div
                key={p.num}
                className={`py-10 pr-12 ${i !== 0 ? "sm:border-l border-white/8 sm:pl-12" : ""}`}
              >
                <span className="mb-6 block text-[11px] font-mono text-white/20">{p.num}</span>
                <h3 className="mb-3 text-base font-bold text-white/70">{p.title}</h3>
                <p className="text-sm text-white/30 leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  )
}

export default UsageSection
