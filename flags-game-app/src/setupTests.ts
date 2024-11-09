import "@testing-library/jest-dom";
import { TextEncoder } from "util";

global.TextEncoder = TextEncoder;
global.TransformStream = global.TransformStream || function () {}; // Añadir esta línea
global.BroadcastChannel = global.BroadcastChannel || function () {}; // Añadir esta línea
