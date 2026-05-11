import { useState, useEffect, useRef, useCallback } from "react"

function cn(...classes) {
  return classes.filter(Boolean).join(" ")
}

export function InteractiveGridPattern({
  cellSize = 48,
  className,
  squaresClassName,
  ...props
}) {
  const svgRef = useRef(null)
  const [dims, setDims] = useState({ w: 0, h: 0 })
  const [hoveredSquare, setHoveredSquare] = useState(null)

  // Measure the SVG's rendered size
  useEffect(() => {
    const el = svgRef.current
    if (!el) return
    const ro = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect
      setDims({ w: width, h: height })
    })
    ro.observe(el)
    return () => ro.disconnect()
  }, [])

  const cols = dims.w > 0 ? Math.ceil(dims.w / cellSize) + 1 : 0
  const rows = dims.h > 0 ? Math.ceil(dims.h / cellSize) + 1 : 0
  const total = cols * rows

  // Compute hovered cell from raw mouse coordinates — works even when
  // the SVG is covered by pointer-events-none overlay layers
  const handleMouseMove = useCallback(
    (e) => {
      const el = svgRef.current
      if (!el) return
      const rect = el.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      const col = Math.floor(x / cellSize)
      const row = Math.floor(y / cellSize)
      if (col >= 0 && col < cols && row >= 0 && row < rows) {
        setHoveredSquare(row * cols + col)
      }
    },
    [cellSize, cols, rows]
  )

  const handleMouseLeave = useCallback(() => setHoveredSquare(null), [])

  // Attach listeners to the parent container (the full-screen div in HeroSection)
  // so they fire regardless of what's layered on top
  useEffect(() => {
    const el = svgRef.current
    if (!el) return
    const parent = el.parentElement
    if (!parent) return
    parent.addEventListener("mousemove", handleMouseMove)
    parent.addEventListener("mouseleave", handleMouseLeave)
    return () => {
      parent.removeEventListener("mousemove", handleMouseMove)
      parent.removeEventListener("mouseleave", handleMouseLeave)
    }
  }, [handleMouseMove, handleMouseLeave])

  return (
    <svg
      ref={svgRef}
      className={cn("absolute inset-0 h-full w-full pointer-events-none", className)}
      {...props}
    >
      {total > 0 &&
        Array.from({ length: total }).map((_, index) => {
          const col = index % cols
          const row = Math.floor(index / cols)
          const x = col * cellSize
          const y = row * cellSize
          const isHovered = hoveredSquare === index

          return (
            <rect
              key={index}
              x={x}
              y={y}
              width={cellSize}
              height={cellSize}
              fill={isHovered ? "rgba(255,255,255,0.07)" : "transparent"}
              stroke="rgba(255,255,255,0.04)"
              strokeWidth="1"
              style={{
                transition: isHovered
                  ? "fill 60ms ease-out"
                  : "fill 800ms ease-out",
              }}
              className={squaresClassName}
            />
          )
        })}
    </svg>
  )
}
