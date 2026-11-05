type Item = { id: string };
const chained = { id: "fixture" } as unknown as Item;
const widened: unknown = { id: "fixture" };
const recovered = widened as Item;
export { chained, recovered };
