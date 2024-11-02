import { ARView } from "./ARView";
import BottomTextField from "./BottomTextField";
import LeftDrawer from "./LeftDrawer";

function App() {
  return (
    <>
      <LeftDrawer />
      <ARView
        markers={[
          [0, 0, 0],
          [10, 0, 0],
          [0, 10, 0],
          [0, 0, 10]
        ]}
        active={0}
      />
      <BottomTextField />
    </>
  );
}

export default App;
