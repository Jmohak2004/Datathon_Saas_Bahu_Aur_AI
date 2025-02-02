import { cn } from "./lib/utils";
import React, { useEffect, useRef, useState, useCallback } from "react";
import { createNoise3D } from "simplex-noise";

export const CombinedBackground = ({
  children,
  className,
  containerClassName,
  colors,
  waveWidth,
  backgroundFill,
  blur = 10,
  speed = "fast",
  waveOpacity = 0.5,
  starDensity = 0.00015,
  allStarsTwinkle = true,
  twinkleProbability = 0.7,
  minTwinkleSpeed = 0.5,
  maxTwinkleSpeed = 1,
  ...props
}) => {
  const noise = createNoise3D();
  const waveCanvasRef = useRef(null);
  const starCanvasRef = useRef(null);
  const [stars, setStars] = useState([]);
  
  let w, h, nt, i, x, waveCtx;
  
  const getSpeed = () => {
    switch (speed) {
      case "slow":
        return 0.001;
      case "fast":
        return 0.002;
      default:
        return 0.001;
    }
  };

  const generateStars = useCallback((width, height) => {
    const area = width * height;
    const numStars = Math.floor(area * starDensity);
    return Array.from({ length: numStars }, () => {
      const shouldTwinkle = allStarsTwinkle || Math.random() < twinkleProbability;
      return {
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 0.05 + 0.5,
        opacity: Math.random() * 0.5 + 0.5,
        twinkleSpeed: shouldTwinkle
          ? minTwinkleSpeed + Math.random() * (maxTwinkleSpeed - minTwinkleSpeed)
          : null,
      };
    });
  }, [starDensity, allStarsTwinkle, twinkleProbability, minTwinkleSpeed, maxTwinkleSpeed]);

  const waveColors = colors ?? [
    "#38bdf8",
    "#818cf8",
    "#c084fc",
    "#e879f9",
    "#22d3ee",
  ];

  const initWaves = () => {
    const canvas = waveCanvasRef.current;
    waveCtx = canvas.getContext("2d");
    w = waveCtx.canvas.width = window.innerWidth;
    h = waveCtx.canvas.height = window.innerHeight;
    waveCtx.filter = `blur(${blur}px)`;
    nt = 0;
  };

  const drawWave = (n) => {
    nt += getSpeed();
    for (i = 0; i < n; i++) {
      waveCtx.beginPath();
      waveCtx.lineWidth = waveWidth || 50;
      waveCtx.strokeStyle = waveColors[i % waveColors.length];
      for (x = 0; x < w; x += 5) {
        var y = noise(x / 800, 0.3 * i, nt) * 100;
        waveCtx.lineTo(x, y + h * 0.5);
      }
      waveCtx.stroke();
      waveCtx.closePath();
    }
  };

  const renderWaves = () => {
    waveCtx.fillStyle = "transparent";
    waveCtx.globalAlpha = waveOpacity || 0.5;
    waveCtx.fillRect(0, 0, w, h);
    drawWave(5);
    return requestAnimationFrame(renderWaves);
  };

  useEffect(() => {
    // Initialize waves
    initWaves();
    const waveAnimationId = renderWaves();

    // Initialize stars
    const canvas = starCanvasRef.current;
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    setStars(generateStars(canvas.width, canvas.height));

    // Handle resize
    const handleResize = () => {
      // Update waves
      w = waveCanvasRef.current.width = window.innerWidth;
      h = waveCanvasRef.current.height = window.innerHeight;
      waveCtx.filter = `blur(${blur}px)`;

      // Update stars
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      setStars(generateStars(canvas.width, canvas.height));
    };

    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(waveAnimationId);
      window.removeEventListener('resize', handleResize);
    };
  }, [generateStars]);

  // Render stars
  useEffect(() => {
    const canvas = starCanvasRef.current;
    const ctx = canvas.getContext("2d");
    
    const renderStars = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((star) => {
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
        ctx.fill();

        if (star.twinkleSpeed !== null) {
          star.opacity = 0.5 + Math.abs(Math.sin((Date.now() * 0.001) / star.twinkleSpeed) * 0.5);
        }
      });

      return requestAnimationFrame(renderStars);
    };

    const starAnimationId = renderStars();
    return () => cancelAnimationFrame(starAnimationId);
  }, [stars]);

  const [isSafari, setIsSafari] = useState(false);
  useEffect(() => {
    setIsSafari(
      typeof window !== "undefined" &&
      navigator.userAgent.includes("Safari") &&
      !navigator.userAgent.includes("Chrome")
    );
  }, []);

  return (
    <div className={cn("h-screen flex flex-col items-center justify-center", containerClassName)}>
      <canvas
        ref={starCanvasRef}
        className="absolute inset-0 z-0 bg-black"
      />
      <canvas
        ref={waveCanvasRef}
        className="absolute inset-0 z-10"
        style={{
          ...(isSafari ? { filter: `blur(${blur}px)` } : {}),
        }}
      />
      <div className={cn("relative z-20", className)} {...props}>
        {children}
      </div>
    </div>
  );
};

export default CombinedBackground;