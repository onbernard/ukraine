import { csv } from "d3"

export async function load({ fetch, params }) {
    const russia = await csv("http://localhost:8000/russia")
    const babies = await csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/5_OneCatSevNumOrdered_wide.csv");
    return {russia, babies};
}