"use client";

import * as React from "react";
import { Toaster, toast as shadcnToast } from "react-hot-toast";

export { shadcnToast as toast };

export function Toast() {
  return <Toaster />;
}
