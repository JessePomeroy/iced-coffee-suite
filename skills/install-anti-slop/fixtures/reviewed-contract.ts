type Status = "open" | "closed";
export const statusLabels: Record<Status, string> = { open: "Open", closed: "Closed" };
export const pending: Record<string, boolean> = { fixture: false };
export function opaqueResult(): unknown { return { id: "fixture" }; }

interface VendorObject { id: string; unusedMethod(): void }
// This partial fixture deliberately exercises only the vendor id boundary.
export const partialVendor = { id: "fixture" } as unknown as VendorObject;
