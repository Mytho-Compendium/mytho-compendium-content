import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";

/**
 * Entry point for the Mytho Compendium shared capability pack.
 *
 * This package registers no tools/commands/events of its own. Its only job is
 * to exist as a loadable extension entry point so that omp's `omp-plugins`
 * discovery provider picks up the sibling capability directories next to this
 * file: agents/, commands/, skills/, rules/. See the README.md files in each
 * of those directories for naming conventions.
 *
 * Referenced from mytho-compendium-app, mytho-compendium-content, and
 * mytho-compendium-server via each repo's `.omp/config.yml`:
 *
 *   extensions:
 *     - "<absolute-path-to>/mytho-compendium-content/omp-shared"
 */
export default function mythoSharedPack(_pi: ExtensionAPI) {
  // No tools/commands/events registered here.
  // Capability discovery of agents/, commands/, skills/, rules/ happens
  // automatically once this package loads through `extensions:`.
}
