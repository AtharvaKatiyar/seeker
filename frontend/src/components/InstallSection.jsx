import { useState } from "react"

function CodeBlock({ code }) {
  const [copied, setCopied] = useState(false)

  const copy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="relative mt-3 border-l border-white/10 pl-5">
      <pre className="overflow-x-auto text-[13px] leading-relaxed text-white/50 font-mono whitespace-pre-wrap">
        <code>{code}</code>
      </pre>
      <button
        onClick={copy}
        className="absolute top-0 right-0 text-[10px] tracking-[0.15em] uppercase text-white/20 hover:text-white/50 transition-colors"
      >
        {copied ? "copied" : "copy"}
      </button>
    </div>
  )
}

const binarySteps = [
  {
    step: "01",
    title: "Install Qt runtime dependencies",
    note: "Ubuntu / Debian",
    code: `sudo apt-get update\nsudo apt-get install -y libxcb-cursor0 libxcb-xinerama0 libxkbcommon-x11-0`,
  },
  {
    step: "02",
    title: "Make executable and run",
    note: "After downloading the binary",
    code: `chmod +x seeker\n./seeker`,
  },
  {
    step: "03",
    title: "Install system-wide",
    note: "Optional",
    code: `sudo install -m 755 seeker /usr/local/bin/seeker\nseeker`,
  },
]

const sourceSteps = [
  {
    step: "01",
    title: "Create and activate virtual environment",
    code: `python3 -m venv .venv\nsource .venv/bin/activate`,
  },
  {
    step: "02",
    title: "Install dependencies",
    code: `pip install psutil PyQt6`,
  },
  {
    step: "03",
    title: "Run",
    code: `python main.py`,
  },
]

function InstallSection() {
  const [tab, setTab] = useState("binary")
  const steps = tab === "binary" ? binarySteps : sourceSteps

  return (
    <section className="bg-[#080808] border-t border-white/8 px-12 py-28 md:px-20">
      <div className="mx-auto max-w-6xl">

        {/* Section label */}
        <div className="mb-16 flex items-center gap-6">
          <span className="text-[11px] font-semibold tracking-[0.25em] uppercase text-white/25">
            Installation
          </span>
          <span className="h-px flex-1 bg-white/8" />
        </div>

        <div className="grid grid-cols-1 gap-20 lg:grid-cols-[1fr_2fr]">

          {/* Left */}
          <div>
            <h2 className="mb-6 text-[clamp(1.75rem,4vw,2.75rem)] font-black leading-tight tracking-tight text-white">
              Get running in minutes
            </h2>
            <p className="mb-10 text-sm leading-relaxed text-white/35">
              Two paths: grab the prebuilt binary (recommended) or run from source.
              Requires Linux.
            </p>

            {/* Requirements */}
            <div>
              <p className="mb-4 text-[11px] font-semibold tracking-[0.2em] uppercase text-white/25">
                Requirements
              </p>
              <div className="space-y-2">
                {["Linux", "Python 3.10+", "psutil", "PyQt6"].map((r) => (
                  <div key={r} className="flex items-center gap-3">
                    <span className="h-px w-4 bg-white/15" />
                    <span className="text-sm font-mono text-white/40">{r}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right */}
          <div>
            {/* Tab switcher — text only, underline style */}
            <div className="mb-12 flex gap-8 border-b border-white/8">
              {[
                { key: "binary", label: "Prebuilt Binary" },
                { key: "source", label: "From Source" },
              ].map((t) => (
                <button
                  key={t.key}
                  onClick={() => setTab(t.key)}
                  className={`pb-3 text-xs font-semibold tracking-[0.15em] uppercase transition-colors border-b-2 -mb-px ${
                    tab === t.key
                      ? "border-white text-white"
                      : "border-transparent text-white/25 hover:text-white/50"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>

            {/* Steps */}
            <div className="space-y-10">
              {steps.map((s) => (
                <div key={s.step} className="grid grid-cols-[2.5rem_1fr] gap-4">
                  <span className="text-[11px] font-mono text-white/20 pt-0.5">{s.step}</span>
                  <div>
                    <div className="flex items-baseline gap-3 mb-1">
                      <h3 className="text-sm font-semibold text-white/70">{s.title}</h3>
                      {s.note && (
                        <span className="text-[11px] text-white/20">{s.note}</span>
                      )}
                    </div>
                    <CodeBlock code={s.code} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default InstallSection
