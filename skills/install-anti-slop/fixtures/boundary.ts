export function decodeName(input: unknown): string {
  if (typeof input !== "string" || input.length === 0) throw new Error("Invalid name");
  return input;
}

type Item = { id: string; kind: "digital" | "print" };
export const item = { id: "fixture", kind: "print" } satisfies Item;
