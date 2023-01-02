<script>
    import ChordChart from "$lib/ChordChart.svelte";
    import StackedAreaChart from "$lib/StackedAreaChart.svelte";
    import { csv, stack } from "d3"
	import { onMount } from "svelte";
    export let data;
</script>


<StackedAreaChart data={data.russia} />
