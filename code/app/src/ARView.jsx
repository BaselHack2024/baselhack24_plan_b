import { ARCanvas, ARMarker } from "@artcom/react-three-arjs";

function Box(props) {
  return (
    <mesh>
      <boxGeometry args={props.marker} />
      <meshStandardMaterial color={props.active ? "yellow" : "blue"} />
    </mesh>
  );
}

export const ARView = (props) => {
  return (
    <ARCanvas
      onCameraStreamReady={() => console.log("Camera stream ready")}
      onCameraStreamError={() => console.error("Camera stream error")}
      sourceType={"webcam"}
    >
      <ambientLight />
      <ARMarker
        debug={true}
        params={{ smooth: true }}
        type={"pattern"}
        patternUrl={"data/patt.hiro"}
        onMarkerFound={() => {
          console.log("marker Found");
        }}
      >
        {props.markers.map((m, i) => (<Box key={i} marker={m} active={i === props.active} />))}
      </ARMarker>
    </ARCanvas>
  );
};
