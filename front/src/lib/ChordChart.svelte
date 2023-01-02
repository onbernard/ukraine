<script>    
    import * as d3 from 'd3'
    import { onMount } from 'svelte';
    import { customChordLayout } from './CustomChord'
    export let width = 800;
    export let height = 900;
    export let data = [
        [0,4,3,2,5,2], //Black Widow
        [4,0,3,2,4,3], //Captain America
        [3,3,0,2,3,3], //Hawkeye
        [2,2,2,0,3,3], //The Hulk
        [5,4,3,3,0,2], //Iron Man
        [2,3,3,3,2,0], //Thor
    ];
    export let names = ["T1","T2","T3","T4","T5","T6"];
    export let colors = ["#301E1E", "#083E77", "#342350", "#567235", "#8B161C", "#DF7C00"];
    const margin = { top: 0, right: 20, bottom: 20, left: 115 };
    const innerHeight = height - margin.top - margin.bottom;
    const innerWidth = width - margin.left - margin.right;
    
    let svgHere;
    $: viewBx = [-width / 2.5, -height / 1.8, width * 1.1, height * 1.1];
    $: outerRadius = Math.min(width, height) * 0.5 - 60;
    $: innerRadius = outerRadius - 10;
    // //generator functions
    // $: chordGen = chord()
    //     .padAngle(10 / innerRadius)
    //     .sortSubgroups(descending)
    //     .sortChords(descending);
    // $: arcGen = arc().innerRadius(innerRadius).outerRadius(outerRadius);
    // $: ribbonGen = ribbon()
    //     .radius(innerRadius - 1)
    //     .padAngle(1 / innerRadius);
    // $: chords = chordGen.matrix(data); //
    // // tick logic
    // $: tickStepX = tickStep(0, sum(data.flat()), 100);
    // let formatValue = format('.1~%');
    // function ticks({ startAngle, endAngle, value }) {
    //     const k = (endAngle - startAngle) / value;
    //     return range(0, value, tickStepX * 2).map((value) => {
    //         return { value, angle: value * k + startAngle };
    //     });
    // }
    // $: colors = d3.scaleOrdinal()
    //     .domain(d3.range(names.length))
    //     .range(colors)
    $: chordGen = customChordLayout()
        .padding(.15)
        .sortChords(d3.descending) 
        .matrix(data);
    
    $: arcGen = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius)
    
    $: ribbonGen = d3.ribbon()
        .radius(innerRadius-1)
        .padAngle(1/innerRadius)
    
    onMount(()=>(console.log(chordGen.chords())))
    let getGradID = (d) => ("linkGrad-" + d.source.index + "-" + d.target.index)
</script>

<div class="canvas-container">
    <svg viewBox={viewBx} {width} {height} bind:this={svgHere}>
        <g transform={`translate(${margin.left},${margin.top})`}>
            {#each chordGen.groups() as group, i}
            <!--Outer arcs-->
            <path fill={colors[i]} d={arcGen(group)} on:click={()=>(console.log(group))}/>
            <!--Arc labels-->
            <g style="transform:rotate({((group.endAngle+group.startAngle) * 90) / Math.PI -90}deg) translate({outerRadius}px,0);">
                <text 
                    fill={colors[i]} 
                    class="group-label"
                    font-weight="bold"
                    dx="25"
                    style="text-anchord:middle;transform:{group.startAngle+group.endAngle > 2*Math.PI? 'rotate(180deg) translate(-95px)': null}"
                >{names[i]}</text>
            </g>
            {/each}
            {#each chordGen.chords() as chord, i}
            <!--Gradient definition-->
            <defs>
                <linearGradient
                    id={getGradID(chord)}
                    gradientUnits="userSpaceOnUse"
                    x1={innerRadius*Math.cos((chord.source.endAngle-chord.source.startAngle)/2+chord.source.startAngle-Math.PI/2)}
                    y1={innerRadius*Math.sin((chord.source.endAngle-chord.source.startAngle)/2+chord.source.startAngle-Math.PI/2)}
                    x2={innerRadius*Math.cos((chord.target.endAngle-chord.target.startAngle)/2+chord.target.startAngle-Math.PI/2)}
                    y2={innerRadius*Math.sin((chord.target.endAngle-chord.target.startAngle)/2+chord.target.startAngle-Math.PI/2)}>
                    <stop offset="0%" stop-color={colors[chord.source.index]}/>
                    <stop offset="100%" stop-color={colors[chord.target.index]}/>
                </linearGradient>
            </defs>
            <!--Inner chords-->
            <path
                fill={"url(#"+getGradID(chord)+")"}
                class="ribbon"
                d={ribbonGen(chord)}
                opacity=".8"
                on:keydown={()=>(null)}
                on:click={()=>(console.log(getGradID(chord)))}/>
            {/each}
        </g>
    </svg>
</div>
<!-- <div class="canvas-container">
    <svg viewBox={viewBx} {width} {height} bind:this={svgHere}>
        <g transform={`translate(${margin.left},${margin.top})`}>
            <g class="outer-arcs">
                {#each chords['groups'] as chord, i}
                    <g class="group">
                        <path fill={colors[i]} d={arcGen(chord)} />
                        <g>
                            {#each ticks(chord) as tick, t}
                                <g
                                    class="tick"
                                    style="transform:rotate({(tick.angle * 180) / Math.PI -
                                        90}deg) translate({outerRadius}px,0);"
                                >
                                    {#if t < 1}
                                        <text
                                            fill={colors[i]}
                                            x="30"
                                            y="5"
                                            class="phone-title"
                                            font-weight="bold"
                                            style="transform:{tick.angle > Math.PI
                                                ? 'rotate(180deg) translate(-95px)'
                                                : null}"
                                        >
                                            {names[i]}
                                        </text>
                                    {/if}
    
                                    <line stroke={colors[i]} x2="6" />
                                </g>
                            {/each}
                        </g>
                    </g>
                {/each}
            </g>
    
            <g class="ribbons" style="fill-opacity:0.4;">
                {#each chords as chord, i}
                    <path fill={colors[chord.source.index]} class="ribbon" d={ribbonGen(chord)} on:click={()=>(console.log("UwU"))}/>
                {/each}
            </g>
        </g>
    </svg>
</div> -->

<style>
    .canvas-container {
        text-align: center;
    }
    svg {
        background: None;
    }
    .ribbon {
        opacity: .9;
    }
    .ribbon:hover {
        opacity: 1;
        stroke: black;
        stroke-width: 1;
    }
</style>