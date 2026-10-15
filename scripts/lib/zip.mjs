// Deterministic zip archives: entries are sorted and share one fixed
// timestamp, so the same content always produces the same bytes and checksum.
import fs from 'node:fs';
import { zipSync, unzipSync } from 'fflate';

const MTIME = new Date(1980, 0, 2);

// entries: [{ path, data: Uint8Array, executable?: boolean }]
export function createZip(entries) {
  const files = {};
  for (const e of [...entries].sort((a, b) => (a.path < b.path ? -1 : 1))) {
    const mode = 0o100000 | (e.executable ? 0o755 : 0o644);
    // Unix mode in the high 16 bits of the external attributes.
    files[e.path] = [e.data, { mtime: MTIME, os: 3, attrs: mode * 0x10000 }];
  }
  return zipSync(files, { level: 9 });
}

export function fileEntry(absPath, archivePath) {
  const stat = fs.statSync(absPath);
  return { path: archivePath, data: fs.readFileSync(absPath), executable: (stat.mode & 0o111) !== 0 };
}

// Returns { path: Uint8Array } for every file in the archive.
export function readZip(absPath) {
  return unzipSync(fs.readFileSync(absPath));
}
