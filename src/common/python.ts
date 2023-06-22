// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

/* eslint-disable @typescript-eslint/naming-convention */
import * as vscode from 'vscode';
import { traceError, traceLog } from './logging';

type Environment = EnvironmentPath & {
    /**
     * Carries details about python executable.
     */
    readonly executable: {
        /**
         * vscode.Uri of the python interpreter/executable. Carries `undefined` in case an executable does not belong to
         * the environment.
         */
        readonly uri: vscode.Uri | undefined;
        /**
         * Bitness if known at this moment.
         */
        readonly bitness: Bitness | undefined;
        /**
         * Value of `sys.prefix` in sys module if known at this moment.
         */
        readonly sysPrefix: string | undefined;
    };
    /**
     * Carries details if it is an environment, otherwise `undefined` in case of global interpreters and others.
     */
    readonly environment:
    | {
        /**
         * Type of the environment.
         */
        readonly type: EnvironmentType;
        /**
         * Name to the environment if any.
         */
        readonly name: string | undefined;
        /**
         * vscode.Uri of the environment folder.
         */
        readonly folderUri: vscode.Uri;
        /**
         * Any specific workspace folder this environment is created for.
         */
        readonly workspaceFolder: vscode.Uri | undefined;
    }
    | undefined;
    /**
     * Carries Python version information known at this moment.
     */
    readonly version: VersionInfo & {
        /**
         * Value of `sys.version` in sys module if known at this moment.
         */
        readonly sysVersion: string | undefined;
    };
    /**
     * Tools/plugins which created the environment or where it came from. First value in array corresponds
     * to the primary tool which manages the environment, which never changes over time.
     *
     * Array is empty if no tool is responsible for creating/managing the environment. Usually the case for
     * global interpreters.
     */
    readonly tools: readonly EnvironmentTools[];
};

/**
 * Derived form of {@link Environment} where certain properties can no longer be `undefined`. Meant to represent an
 * {@link Environment} with complete information.
 */
type ResolvedEnvironment = Environment & {
    /**
     * Carries complete details about python executable.
     */
    readonly executable: {
        /**
         * vscode.Uri of the python interpreter/executable. Carries `undefined` in case an executable does not belong to
         * the environment.
         */
        readonly uri: vscode.Uri | undefined;
        /**
         * Bitness of the environment.
         */
        readonly bitness: Bitness;
        /**
         * Value of `sys.prefix` in sys module.
         */
        readonly sysPrefix: string;
    };
    /**
     * Carries complete Python version information.
     */
    readonly version: ResolvedVersionInfo & {
        /**
         * Value of `sys.version` in sys module if known at this moment.
         */
        readonly sysVersion: string;
    };
};

type EnvironmentsChangeEvent = {
    readonly env: Environment;
    /**
     * * "add": New environment is added.
     * * "remove": Existing environment in the list is removed.
     * * "update": New information found about existing environment.
     */
    readonly type: 'add' | 'remove' | 'update';
};

type ActiveEnvironmentPathChangeEvent = EnvironmentPath & {
    /**
     * Workspace folder the environment changed for.
     */
    readonly resource: vscode.WorkspaceFolder | undefined;
};

/**
 * vscode.Uri of a file inside a workspace or workspace folder itself.
 */
type Resource = vscode.Uri | vscode.WorkspaceFolder;

type EnvironmentPath = {
    /**
     * The ID of the environment.
     */
    readonly id: string;
    /**
     * Path to environment folder or path to python executable that uniquely identifies an environment. Environments
     * lacking a python executable are identified by environment folder paths, whereas other envs can be identified
     * using python executable path.
     */
    readonly path: string;
};

/**
 * Tool/plugin where the environment came from. It can be {@link KnownEnvironmentTools} or custom string which
 * was contributed.
 */
type EnvironmentTools = KnownEnvironmentTools | string;
/**
 * Tools or plugins the Python extension currently has built-in support for. Note this list is expected to shrink
 * once tools have their own separate vscode.extensions.
 */
type KnownEnvironmentTools =
    | 'Conda'
    | 'Pipenv'
    | 'Poetry'
    | 'VirtualEnv'
    | 'Venv'
    | 'VirtualEnvWrapper'
    | 'Pyenv'
    | 'Unknown';

/**
 * Type of the environment. It can be {@link KnownEnvironmentTypes} or custom string which was contributed.
 */
type EnvironmentType = KnownEnvironmentTypes | string;
/**
 * Environment types the Python extension is aware of. Note this list is expected to shrink once tools have their
 * own separate vscode.extensions, in which case they're expected to provide the type themselves.
 */
type KnownEnvironmentTypes = 'VirtualEnvironment' | 'Conda' | 'Unknown';

/**
 * Carries bitness for an environment.
 */
type Bitness = '64-bit' | '32-bit' | 'Unknown';

/**
 * The possible Python release levels.
 */
type PythonReleaseLevel = 'alpha' | 'beta' | 'candidate' | 'final';

/**
 * Release information for a Python version.
 */
type PythonVersionRelease = {
    readonly level: PythonReleaseLevel;
    readonly serial: number;
};

type VersionInfo = {
    readonly major: number | undefined;
    readonly minor: number | undefined;
    readonly micro: number | undefined;
    readonly release: PythonVersionRelease | undefined;
};

type ResolvedVersionInfo = {
    readonly major: number;
    readonly minor: number;
    readonly micro: number;
    readonly release: PythonVersionRelease;
};

interface IExtensionApi {
    ready: Promise<void>;
    debug: {
        getRemoteLauncherCommand(host: string, port: number, waitUntilDebuggerAttaches: boolean): Promise<string[]>;
        getDebuggerPackagePath(): Promise<string | undefined>;
    };
    environments: {
        getActiveEnvironmentPath(resource?: Resource): EnvironmentPath;
        resolveEnvironment(
            environment: Environment | EnvironmentPath | string,
        ): Promise<ResolvedEnvironment | undefined>;
        readonly onDidChangeActiveEnvironmentPath: vscode.Event<ActiveEnvironmentPathChangeEvent>;
    };
}

export interface IInterpreterDetails {
    path?: string[];
    resource?: vscode.Uri;
}

const onDidChangePythonInterpreterEvent = new vscode.EventEmitter<IInterpreterDetails>();
export const onDidChangePythonInterpreter: vscode.Event<IInterpreterDetails> = onDidChangePythonInterpreterEvent.event;

async function activateExtension() {
    const extension = vscode.extensions.getExtension('ms-python.python');
    if (extension) {
        if (!extension.isActive) {
            await extension.activate();
        }
    } else {
        vscode.window.showErrorMessage('Please install the Python extension.');
        return;
    }
    return extension;
}

async function getPythonExtensionAPI(): Promise<IExtensionApi | undefined> {
    const extension = await activateExtension();
    return extension?.exports as IExtensionApi;
}

export async function initializePython(Disposables: vscode.Disposable[]): Promise<void> {
    try {
        const api = await getPythonExtensionAPI();
        if (api) {
            Disposables.push(
                api.environments.onDidChangeActiveEnvironmentPath((e) => {
                    onDidChangePythonInterpreterEvent.fire({ path: [e.path], resource: e.resource?.uri });
                }),
            );
            traceLog('Waiting for interpreter from python extension.');
            onDidChangePythonInterpreterEvent.fire(await getInterpreterDetails());
        }
    } catch (error) {
        traceError('Error initializing python: ', error);
    }
}

export async function resolveInterpreter(interpreter: string[]): Promise<ResolvedEnvironment | undefined> {
    const api = await getPythonExtensionAPI();
    return api?.environments.resolveEnvironment(interpreter[0]);
}

export async function getInterpreterDetails(resource?: vscode.Uri): Promise<IInterpreterDetails> {
    const api = await getPythonExtensionAPI();
    const environment = await api?.environments.resolveEnvironment(
        api?.environments.getActiveEnvironmentPath(resource),
    );
    if (environment?.executable.uri && checkVersion(environment)) {
        return { path: [environment?.executable.uri.fsPath], resource };
    }
    return { path: undefined, resource };
}

export async function getDebuggerPath(): Promise<string | undefined> {
    const api = await getPythonExtensionAPI();
    return api?.debug.getDebuggerPackagePath();
}

export async function runPythonExtensionCommand(command: string, ...rest: any[]) {
    await activateExtension();
    return await vscode.commands.executeCommand(command, ...rest);
}

export function checkVersion(resolved: ResolvedEnvironment | undefined): boolean {
    const version = resolved?.version;
    if (version?.major === 3 && version?.minor >= 7) {
        return true;
    }
    traceError(`Python version ${version?.major}.${version?.minor} is not supported.`);
    traceError(`Selected python path: ${resolved?.executable.uri?.fsPath}`);
    traceError('Supported versions are 3.7 and above.');
    return false;
}