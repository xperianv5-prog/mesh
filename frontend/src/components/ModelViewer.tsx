import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF, Environment, Center } from "@react-three/drei";
import { Suspense, useState } from "react";

function Model({ url, wireframe }: { url: string; wireframe: boolean }) {
  const { scene } = useGLTF(url);
  scene.traverse((o: any) => {
    if (o.isMesh && o.material) o.material.wireframe = wireframe;
  });
  return <primitive object={scene} />;
}

export function ModelViewer({ url }: { url: string }) {
  const [wireframe, setWireframe] = useState(false);

  return (
    <div style={{
      position: "relative",
      width: "100%",
      height: 400,
      background: "#0a0f1a",
      borderRadius: 8,
      overflow: "hidden",
    }}>
      <Canvas camera={{ position: [2, 2, 2], fov: 45 }}>
        <ambientLight intensity={0.6} />
        <directionalLight position={[5, 5, 5]} intensity={1.2} />
        <Suspense fallback={null}>
          <Center>
            <Model url={url} wireframe={wireframe} />
          </Center>
          <Environment preset="city" />
        </Suspense>
        <OrbitControls makeDefault enableDamping />
      </Canvas>

      <div style={{
        position: "absolute",
        top: 8,
        right: 8,
        display: "flex",
        gap: 6,
      }}>
        <button
          onClick={() => setWireframe((w) => !w)}
          style={{ padding: "4px 10px", fontSize: 12, background: "#1e293b" }}
        >
          {wireframe ? "Solid" : "Wireframe"}
        </button>
        <a
          href={url}
          download
          style={{
            padding: "4px 10px",
            fontSize: 12,
            background: "#3b82f6",
            color: "white",
            textDecoration: "none",
            borderRadius: 6,
          }}
        >
          Download
        </a>
      </div>
    </div>
  );
}
