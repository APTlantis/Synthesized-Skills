# Integration, lifecycle and recovery

## Loading paths

For a bundler using the installed Chart.js 4 package:

```javascript
import Chart from 'chart.js/auto';
import { createExampleConfig } from './configs.mjs';

const canvas = document.querySelector('#chart');
const chart = new Chart(canvas, createExampleConfig('bar'));
```

Here `./configs.mjs` means the bundled example module copied into the owning project; adjust the relative import to its actual location. For a smaller bar-only bundle, replace the auto import with explicit registration:

```javascript
import {
  Chart, BarController, BarElement, CategoryScale, LinearScale,
  Title, Legend, Tooltip,
} from 'chart.js';

Chart.register(BarController, BarElement, CategoryScale, LinearScale,
  Title, Legend, Tooltip);
```

Other chart types need their own controllers/elements/scales. An area fill may require `Filler`; a time axis still needs a compatible adapter. Avoid importing both the UMD build and a bundled instance into the same integration. For a plain script, load the installed version's UMD distribution (`dist/chart.umd.min.js` in the tested 4.6.1 package), then use its `Chart` global. Resolve an exact local file or approved pinned distribution rather than adding an unversioned CDN URL by default.

## Container and alternative content

```html
<section aria-labelledby="chart-heading">
  <h2 id="chart-heading">Requests by queue (illustrative)</h2>
  <p id="chart-summary">Of 63 sample requests, General has 28, Billing 19,
    and Technical 16. General has the largest count.</p>
  <div style="position:relative;height:320px;width:100%;min-width:0">
    <canvas id="chart" role="img" aria-label="Requests by queue"
      aria-describedby="chart-summary">
      Requests by queue: General 28, Billing 19, Technical 16.
    </canvas>
  </div>
</section>
```

Keep the dedicated chart container for the canvas; place descriptions and data tables outside it. Match this example with the bar config or update every textual alternative to the actual values. A production table or summary should derive from the same source as the chart and update with it. Provide actual HTML table structure when detailed values are needed. A role or label alone does not expose dataset values or make canvas interaction keyboard-accessible.

Resize the container instead of assigning CSS-like values to canvas width/height attributes. Check nonzero size in hidden tabs and call `resize()` after the chart becomes visible if needed. Flex/grid children may need `min-width: 0`. For print, test explicit sizing and restoration rather than assuming responsive screen sizing survives printing.

## Update and teardown

```javascript
chart.data.labels = nextLabels;
chart.data.datasets[0].data = nextValues;
chart.update('none');

// At the owning component's teardown, and before reusing the canvas:
chart.destroy();
```

Replace `nextLabels` and `nextValues` with validated application values. Changing scale IDs or types can invalidate stored scale references; reacquire them afterwards. Destroy any auxiliary event listeners, observers, HTML tooltips or legend nodes owned by the integration too. Framework wrappers may already manage chart creation, update and teardown: follow the installed wrapper's documented lifecycle and do not assume a raw example proves wrapper compatibility.

Preserve callbacks by avoiding JSON cloning. For async loads, prevent late responses from recreating a disposed chart and keep loading/error/empty UI explicit. On the server, defer browser rendering to the client or use a supported canvas backend with its own fonts and dependency checks.

## Interactions and export

Test hover/tap behavior required by the product, tooltip units and precision, legend visibility changes, and any click callback's selected dataset/index. Supply accessible HTML controls for required keyboard interactions, synchronized with chart visibility. Treat strings as text when producing external HTML legends/tooltips. Inspect plugin APIs against the installed version instead of assuming core supports annotations or zoom.

`chart.toBase64Image()` returns a raster image URL, normally PNG. Export after rendering completes; wait for animation completion or use a deliberate nonanimated export. Canvas CSS background does not become painted pixels automatically. For an opaque export, draw the background using an appropriate plugin or an export canvas; preserve desired transparency. Account for pixel ratio, fonts and output dimensions. Do not call the result SVG, PDF, or editable vector artwork.

## Symptom-based recovery

| Symptom | Inspect first | Repair |
|---|---|---|
| Controller/scale not registered | Modular imports and registration | Register the required components or use the approved auto path |
| Canvas already in use | Existing instance and component ownership | Destroy the owning instance before reuse; avoid competing wrappers |
| Blank or tiny chart | Data, canvas context, hidden parent and container dimensions | Repair the data or nonzero layout; resize after reveal |
| Endless growth or blur | Parent sizing, aspect ratio and canvas CSS | Give the canvas a dedicated controlled container |
| Time scale adapter error | Adapter/library presence and loading order | Load a compatible adapter; do not disguise time as categories |
| Old options appear ignored | Resolved version and current option paths | Migrate only the affected options using the correct version guide |
| Line bridges a missing observation | Null conversion and spanGaps | Preserve missing data and choose gap behavior deliberately |
| Export is transparent or incomplete | Painted background, animation and fonts | Render/export at the correct stage with explicit background policy |

If the environment cannot render, deliver source and a precise validation limit. Do not disable security settings or upload private data merely to obtain a preview.
