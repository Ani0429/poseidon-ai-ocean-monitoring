import { Canvas, useFrame } from "@react-three/fiber";
import { useRef } from "react";

/* Single Fish */
function Fish({ x, startY }) {
  const ref = useRef();

  useFrame(({ viewport }) => {
    if (!ref.current) return;

    // Move fish DOWN continuously
    ref.current.position.y -= 0.01;

    // Reset fish to top when it goes out of view
    if (ref.current.position.y < -viewport.height) {
      ref.current.position.y = viewport.height;
    }
  });

  return (
    <mesh ref={ref} position={[x, startY, -5]}>
      {/* Simple fish shape */}
      <coneGeometry args={[0.12, 0.35, 16]} />
      <meshStandardMaterial color="#7dd3fc" />
    </mesh>
  );
}

/* Fish Layer */
export default function FishScene() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 60 }}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 2,
        pointerEvents: "none",
      }}
    >
      <ambientLight intensity={0.7} />
      <directionalLight position={[3, 5, 5]} intensity={1} />

      {/* Multiple fish */}
      <Fish x={-1.5} startY={2} />
      <Fish x={0} startY={0} />
      <Fish x={1.2} startY={-2} />
      <Fish x={-0.6} startY={-4} />
      <Fish x={0.8} startY={4} />
    </Canvas>
  );
}
