// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import * as child_process from 'child_process';
import { spawn } from 'child_process';
import * as python from './common/python';


let pythonPath: string = "";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, extension "miuc" is now active!');

    // first check if has python environment and miuc installed
    await checkMiucEnvironment();

    let disposable = vscode.commands.registerCommand('miuc.myFunction', getUrlTitle);
    context.subscriptions.push(disposable);
    // 注册按键绑定
    context.subscriptions.push(
        vscode.commands.registerCommand('miuc.myKeyBinding', () => {
            getUrlTitle();
        })
    );
}

async function checkMiucEnvironment() {

    const pythonInterpreterDetails = await python.getInterpreterDetails(vscode.Uri.file(''));

    if (!pythonInterpreterDetails.path) {
        return;
    }
    // get the first python interpreter
    const pythonInterpreterPath = pythonInterpreterDetails.path[0];
    console.log('activate python interpreter path is ' + pythonInterpreterPath);
    const isMiuCInstalled = await isPackageInstalled(pythonInterpreterPath, 'miuc');

    if (!isMiuCInstalled) {
        const installMiuC = await vscode.window.showInformationMessage(
            'The "miuc" package is not installed. Do you want to install it?',
            'Yes', 'No'
        );

        if (installMiuC === 'Yes') {
            await installPackage(pythonInterpreterPath, 'miuc');
        }
    } else {
        console.log("miuc is installed");
    }
    pythonPath = pythonInterpreterPath;
}


function getUrlTitle() {
    const clipboardTextPromise = vscode.env.clipboard.readText();

    clipboardTextPromise.then(text => {
        if (isWebUrl(text)) {
            // call miuc
            const command = `${pythonPath} -m miuc.main ${text}`;
            // const command = `miuc ${text}`;
            child_process.exec(command, (error, stdout) => {
                if (error) {
                    console.error(`miuc error：${error.message}`);
                    insertText(`[unknown](${text})`, true);
                    return;
                }

                // get result [title](url) from miuc
                const result = stdout.trim();
                console.log(`miuc return：${result}`);
                
                const title = result.slice(1, result.lastIndexOf(']'));
                // console.log("title", title);
                // insert
                if (title === "unknown") {
                    insertText(result, true);
                } else {
                    insertText(result, false);
                }
                
            });
        } else {
            insertText(text, false);
        }
    });
}

function insertText(text: string, isSelected: boolean) {
    const editor = vscode.window.activeTextEditor;
    if (editor) {
        editor.edit(editBuilder => {
            const position = editor.selection.active;
            editBuilder.insert(position, text);
        });
        if (isSelected) {
            const position = editor.selection.active;
            const startPosition = position.translate(0, 1);
            const endPosition = position.translate(0, text.lastIndexOf(']'));
            editor.selection = new vscode.Selection(startPosition, endPosition);
        }
    }
}

function isWebUrl(str: string): boolean {
    const urlRegex = /^https?:\/\/[\w\-_]+(?:\.[\w\-_]+)+(?:[\w\-\.,@?^=%&:\/~\+#]*[\w\-\@?^=%&\/~\+#])?$/;
    return urlRegex.test(str);
}


async function isPackageInstalled(pythonPath: string, packageName: string): Promise<boolean> {


    return new Promise<boolean>((resolve) => {
        const process = spawn(pythonPath, ['-m', 'pip', 'show', packageName]);
        process.on('close', (code) => {
            resolve(code === 0);
        });
    });
}

async function installPackage(pythonPath: string, packageName: string): Promise<void> {
    const terminal = vscode.window.createTerminal({ name: 'Package Installation' });
    terminal.sendText(`${pythonPath} -m pip install ${packageName}`);
}



// This method is called when your extension is deactivated
export function deactivate() { }
