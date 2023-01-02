<script>
	import { onMount } from 'svelte';
    import { area, timeParse, scaleTime, brushX, schemeBrBG, schemeBlues, schemeGreys, schemeSpectral, scaleOrdinal, schemeSet3, stack, scaleLinear, extent, axisBottom, axisLeft, select } from 'd3';
    export let width = 2000;
    export let height = 1300;
    export let data;

    const margin = {top:30, right:200, bottom:30, left:60};
    let innerHeight = height - margin.top - margin.bottom;
    let innerWidth = width - margin.left - margin.right;

    let svgElement;
    let hovered=null;

    // GENERAL
    const keys = data.columns.slice(1);
    $: color = scaleOrdinal()
        .domain(keys)
        .range(schemeSpectral[9]);

    const parser = timeParse("%Y%m%d")
    data.forEach((d)=>{
        d.date = parser(d.date)
    })
    const stackedData = stack()
        .keys(keys)
        (data);
    // AXIS
    // x axis
    let xAxis;
    let yAxis;
    $: x = scaleTime()
        .domain(extent(data, (d)=>(d.date)))
        .range([0, innerWidth]);
    $: y = scaleLinear()
        .domain([0, 10000])
        .range([innerHeight, 0])
    $: if (xAxis) {
        select(xAxis).call(axisBottom(x).ticks(5))
    }
    $: if (yAxis) {
        select(yAxis).call(axisLeft(y).ticks(5))
    }
    // BRUSHING AND CHART
    // Area generator
    const areaGen = area()
        .x( (d) => (x(d.data.date)) )
        .y0( (d) => (y(d[0])) )
        .y1( (d) => (y(d[1])) )


    
    onMount(()=>{
        console.log(data)
    });
</script>


<div class="svg-container">
    <svg {width} {height} bind:this={svgElement}>
        <g
        transform="translate({margin.left},{margin.top})">
        <defs>
            <clipPath id="clip">
                <rect width={innerWidth} height={innerHeight} x=0 y=0/>
            </clipPath>
        </defs>
        <g clip-path="url(#clip)">
            {#each stackedData as d,i}
            <path
            class="area"
            class:hovered="{hovered===d.key}"
            fill={color(d.key)}
            d={areaGen(d)}
            on:mouseenter={()=>(hovered=d.key)}
            on:mouseleave={()=>(hovered=null)}/>
            {/each}
        </g>
    </g>
    {#each keys as k,i}
    <rect
        x={margin.left + innerWidth}
        y={10+i*30}
        width="20"
        height="20"
        style="fill: {color(k)};"
        on:mouseenter={()=>(hovered=k)}
        on:mouseleave={()=>(hovered=null)}
        on:click={()=>console.log(stackedData[i])}/>
    <text
        x={margin.left + innerWidth+50}
        y={10+i*30 + 15}
        style="fill: {color(k)};"
        on:mouseenter={()=>(hovered=k)}
        on:mouseleave={()=>(hovered=null)}>
        {k}
    </text>
    {/each}
    <g 
        class="xAxis"
        bind:this={xAxis}
        transform="translate({margin.left},{height-margin.bottom})">
    </g>
    <g
        class="yAxis"
        bind:this={yAxis}
        transform="translate({margin.left},{margin.top})">
    </g>
    </svg>
</div>

<style>
    .svg-container {
        text-align: center;
    }

    svg {
        background-color: #eee5;
    }

    .area {
        opacity: .8;
    }

    .hovered {
        stroke: black;
        stroke-width: 1px;
        opacity: 1;
    }

</style>