// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import * as child_process from 'child_process';
import { spawn } from 'child_process';

let originUrl: string = "";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, extension "miuc" is now active!');

    let disposable1 = vscode.commands.registerCommand('miuc.myFunction', getUrlTitle);
    context.subscriptions.push(disposable1);
    // register key map
    context.subscriptions.push(
        vscode.commands.registerCommand('miuc.myKeyBinding', () => {
            getUrlTitle();
        })
    );

    // tab 跳转到结尾
    let disposable2 = vscode.commands.registerCommand('miuc.tabKey', () => {
        const editor = vscode.window.activeTextEditor;
        console.log("catch tab key");
        if (editor) {
            // 找到高亮的文本的行
            const selection = editor.selection;
            const currentLine = editor.document.lineAt(selection.active.line);
            const lineText = currentLine.text;
            // 找到下一个右括号的位置
            const nextParenthesisIndex = lineText.indexOf(")", selection.active.character + 1);
            if (nextParenthesisIndex !== -1) {
                // 将光标移动到结尾的右括号的位置
                const nextPosition = new vscode.Position(selection.active.line, nextParenthesisIndex + 1);
                editor.selection = new vscode.Selection(nextPosition, nextPosition);
            }
        }
    });

    // esc 恢复为原始 url
    let disposable3 = vscode.commands.registerCommand('miuc.escKey', () => {
        const editor = vscode.window.activeTextEditor;
        // console.log("catch esc key");
        if (editor && originUrl.length > 0) {
            const selection = editor.selection;
            // 找到高亮的文本的行的内容, 替换为原始 url
            const currentLine = editor.document.lineAt(selection.active.line);
            const lineText = currentLine.text;
            const nextParenthesisIndex = lineText.indexOf(")", selection.active.character + 1);
            // 判断一下当前的 url 是否为原始 url
            const currentUrl = lineText.substring(selection.active.character + 2, nextParenthesisIndex);
            // console.log("current url: " + currentUrl);
            // console.log("origin url: " + originUrl);
            if (currentUrl === originUrl) {
                editor.edit((editBuilder) => {
                    editBuilder.replace(new vscode.Range(selection.active.line, selection.anchor.character - 1, selection.active.line, nextParenthesisIndex + 1), originUrl);
                });
                // 光标跳至结尾
                const nextPosition = new vscode.Position(selection.active.line, nextParenthesisIndex + 1);
                editor.selection = new vscode.Selection(nextPosition, nextPosition);
            }
        }
    });

    context.subscriptions.push(disposable2);
    context.subscriptions.push(disposable3);
    // register disposable into subscription, and then 
    // check if has python environment and miuc installed
    await checkMiucEnvironment();
}

async function checkMiucEnvironment() {

    // use global python interpreter to install miuc
    const isMiuCInstalled = await isPackageInstalled('miuc');
    // console.log(isMiuCInstalled);
    if (!isMiuCInstalled) {
        // install miuc if not installed in current python environment
        const installMiuC = await vscode.window.showInformationMessage(
            'The "miuc" package is not installed. Do you want to install it?',
            'Yes', 'No'
        );

        if (installMiuC === 'Yes') {
            await installPackage('miuc');
        }
    } else {
        const miucVersion = await getMiucVersion();
        console.log("miuc version: " + miucVersion);
    }
}

async function getMiucVersion(): Promise<string> {
    // miuc -v
    return new Promise<string>((resolve) => {
        const process = spawn('miuc', ['-v']);
        process.on('close', (code) => {
            resolve(`miuc version: ${code}`);
        });
    });
}


function getUrlTitle() {
    const clipboardTextPromise = vscode.env.clipboard.readText();

    clipboardTextPromise.then(text => {
        if (isWebUrl(text)) {
            // call miuc
            const command = `miuc "${text}"`;
            // const command = `miuc ${text}`;
            child_process.exec(command, (error, stdout) => {
                if (error) {
                    // console.error(`miuc error:${error.message}`);
                    insertText(`[unknown](${text})`, true);
                    return;
                }

                // get result [title](url) from miuc, use utf8 format
                const result = stdout.trim();
                // insert
                originUrl = text;
                insertText(result, true);
            });
        } else {
            originUrl = "";
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
    const urlRegex = /^https?:\/\/[\w\-_]+(?:\.[\w\-_]+)+(?:[\w\-\.,@?^=%&:\/~\+#]*[\w\-\@?^=%&\/~\+#])?(?:;[\w\-\.,@?^=%&:\/~\+#=]*)?$/;
    return urlRegex.test(str);
}


async function isPackageInstalled(packageName: string): Promise<boolean> {
    // check by pip show
    return new Promise<boolean>((resolve) => {
        const process = spawn('pip', ['show', packageName]);
        process.on('close', (code) => {
            resolve(code === 0);
        });
    });
}

async function installPackage(packageName: string): Promise<void> {
    const terminal = vscode.window.createTerminal({ name: 'Package Installation' });
    terminal.sendText(`pip install ${packageName}`);
}



// This method is called when your extension is deactivated
export function deactivate() { }
