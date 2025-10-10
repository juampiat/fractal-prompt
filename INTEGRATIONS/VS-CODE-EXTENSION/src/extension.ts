import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
    console.log('FRACTAL-PROMPT extension is now active! 🤝');

    // Register commands
    let initProject = vscode.commands.registerCommand('fractal-prompt.init', () => {
        initializeProject();
    });

    let createBackup = vscode.commands.registerCommand('fractal-prompt.backup', (uri: vscode.Uri) => {
        createFractalBackup(uri);
    });

    let createCheckpoint = vscode.commands.registerCommand('fractal-prompt.checkpoint', () => {
        createCollaborationCheckpoint();
    });

    let validateCompliance = vscode.commands.registerCommand('fractal-prompt.validate', () => {
        validateFractalCompliance();
    });

    // Register webview provider for sidebar
    const provider = new FractalPromptProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('fractal-prompt-sidebar', provider)
    );

    context.subscriptions.push(initProject, createBackup, createCheckpoint, validateCompliance);

    // Auto-backup on file save (configurable)
    const config = vscode.workspace.getConfiguration('fractal-prompt');
    if (config.get('autoBackup', true)) {
        let autoBackup = vscode.workspace.onDidSaveTextDocument((document) => {
            if (document.fileName.endsWith('.md') || document.fileName.endsWith('.py') || document.fileName.endsWith('.js')) {
                vscode.window.showInformationMessage('🔄 FRACTAL-PROMPT: Auto-backup created', 'View').then(selection => {
                    if (selection === 'View') {
                        vscode.commands.executeCommand('fractal-prompt.backup', vscode.Uri.file(document.fileName));
                    }
                });
            }
        });
        context.subscriptions.push(autoBackup);
    }
}

async function initializeProject() {
    const projectName = await vscode.window.showInputBox({
        prompt: 'Enter project name',
        placeHolder: 'my-awesome-project'
    });

    if (!projectName) {
        return;
    }

    const projectType = await vscode.window.showQuickPick(
        ['general', 'web', 'mobile', 'data', 'ai'],
        { placeHolder: 'Select project type' }
    );

    if (!projectType) {
        return;
    }

    // Create project directory
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    const projectDir = path.join(workspaceFolder.uri.fsPath, projectName);

    try {
        // Create directory
        if (!fs.existsSync(projectDir)) {
            fs.mkdirSync(projectDir, { recursive: true });
        }

        // Copy FRACTAL-PROMPT templates
        await copyFractalTemplates(projectDir);

        vscode.window.showInformationMessage(
            `🎉 FRACTAL-PROMPT project "${projectName}" initialized!`,
            'Open Project'
        ).then(selection => {
            if (selection === 'Open Project') {
                vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(projectDir));
            }
        });

    } catch (error) {
        vscode.window.showErrorMessage(`Failed to initialize project: ${error}`);
    }
}

async function createFractalBackup(uri?: vscode.Uri) {
    const filePath = uri?.fsPath || vscode.window.activeTextEditor?.document.fileName;

    if (!filePath) {
        vscode.window.showWarningMessage('No file selected for backup');
        return;
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const fileName = path.basename(filePath);
    const backupDir = path.join(path.dirname(filePath), 'backups');

    try {
        // Create backups directory if it doesn't exist
        if (!fs.existsSync(backupDir)) {
            fs.mkdirSync(backupDir, { recursive: true });
        }

        const backupPath = path.join(backupDir, `${fileName}_${timestamp}`);
        fs.copyFileSync(filePath, backupPath);

        vscode.window.showInformationMessage(
            `✅ FRACTAL-PROMPT backup created: ${backupPath}`,
            'View Backups'
        ).then(selection => {
            if (selection === 'View Backups') {
                vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(backupDir));
            }
        });

    } catch (error) {
        vscode.window.showErrorMessage(`Failed to create backup: ${error}`);
    }
}

async function createCollaborationCheckpoint() {
    const checkpointContent = `# 🤝 FRACTAL-PROMPT Collaboration Checkpoint

## 📅 Date: ${new Date().toISOString().split('T')[0]}

### ✅ Completed Tasks
- [ ] Document what was accomplished

### 🔄 Current Work
- [ ] Current focus and progress

### 🚧 Challenges
- [ ] Issues encountered and how they were resolved

### 💡 Learnings
- [ ] New insights or knowledge gained

### 🎯 Next Steps
- [ ] Planned work for next session

### 🤝 Collaboration Notes
- [ ] How human-AI collaboration is working
- [ ] Areas for improvement
- [ ] Successful patterns to repeat

---
*Generated by FRACTAL-PROMPT VS Code Extension*
`;

    const document = await vscode.workspace.openTextDocument({
        content: checkpointContent,
        language: 'markdown'
    });

    await vscode.window.showTextDocument(document);
}

async function validateFractalCompliance() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    const requiredFiles = [
        'PROJECT_INITIATION.md',
        'fractal-config.json',
        'README.md'
    ];

    const missingFiles: string[] = [];
    const presentFiles: string[] = [];

    for (const file of requiredFiles) {
        const filePath = path.join(workspaceFolder.uri.fsPath, file);
        if (fs.existsSync(filePath)) {
            presentFiles.push(file);
        } else {
            missingFiles.push(file);
        }
    }

    let message = '## FRACTAL-PROMPT Compliance Report\n\n';

    if (presentFiles.length > 0) {
        message += `### ✅ Present Files:\n${presentFiles.map(f => `- ${f}`).join('\n')}\n\n`;
    }

    if (missingFiles.length > 0) {
        message += `### ❌ Missing Files:\n${missingFiles.map(f => `- ${f}`).join('\n')}\n\n`;
        message += `### 💡 To fix:\n`;
        message += `Run: fractal-cli init <project-name>\n`;
    }

    if (missingFiles.length === 0) {
        message += `🎉 Project is FRACTAL-PROMPT compliant!\n`;
    }

    const document = await vscode.workspace.openTextDocument({
        content: message,
        language: 'markdown'
    });

    await vscode.window.showTextDocument(document);
}

async function copyFractalTemplates(destinationDir: string) {
    // This would typically download or copy from the FRACTAL-PROMPT repository
    // For now, we'll create basic templates

    const templates = {
        'PROJECT_INITIATION.md': `# 🚀 FRACTAL-PROMPT Project Initiation

## 🎯 Project: ${path.basename(destinationDir)}

**Started:** ${new Date().toISOString().split('T')[0]}
**FRACTAL-PROMPT Version:** 1.0

### 🤝 Collaboration Setup
- Human-AI partnership established
- Communication protocols defined
- Backup strategies implemented

---
*Initialized with FRACTAL-PROMPT VS Code Extension*
`,
        'fractal-config.json': JSON.stringify({
            project_name: path.basename(destinationDir),
            fractal_version: "1.0",
            created_date: new Date().toISOString(),
            ide_integration: "vscode-extension",
            backup_automation: true
        }, null, 2)
    };

    for (const [fileName, content] of Object.entries(templates)) {
        const filePath = path.join(destinationDir, fileName);
        fs.writeFileSync(filePath, content);
    }
}

class FractalPromptProvider implements vscode.WebviewViewProvider {
    constructor(private extensionUri: vscode.Uri) {}

    resolveWebviewView(webviewView: vscode.WebviewView): void {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this.extensionUri]
        };

        webviewView.webview.html = this.getWebviewContent();

        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async (message) => {
            switch (message.type) {
                case 'init-project':
                    vscode.commands.executeCommand('fractal-prompt.init');
                    break;
                case 'create-backup':
                    vscode.commands.executeCommand('fractal-prompt.backup');
                    break;
                case 'create-checkpoint':
                    vscode.commands.executeCommand('fractal-prompt.checkpoint');
                    break;
            }
        });
    }

    private getWebviewContent(): string {
        return `
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>FRACTAL-PROMPT</title>
                <style>
                    body { font-family: var(--vscode-font-family); padding: 20px; }
                    .button { background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; padding: 10px 20px; margin: 5px; cursor: pointer; }
                    .button:hover { background: var(--vscode-button-hoverBackground); }
                    .header { color: var(--vscode-textLink-foreground); font-size: 18px; margin-bottom: 20px; }
                </style>
            </head>
            <body>
                <div class="header">🤝 FRACTAL-PROMPT Collaboration</div>

                <button class="button" onclick="initProject()">🚀 Initialize Project</button>
                <button class="button" onclick="createBackup()">💾 Create Backup</button>
                <button class="button" onclick="createCheckpoint()">📋 Collaboration Checkpoint</button>

                <div style="margin-top: 30px; padding: 15px; background: var(--vscode-textBlockQuote-background);">
                    <h3>💡 FRACTAL-PROMPT Principles</h3>
                    <ul>
                        <li><strong>Honest Collaboration:</strong> Admit limitations and seek help</li>
                        <li><strong>Rigorous Protocols:</strong> Backup, validate, document</li>
                        <li><strong>Continuous Learning:</strong> Every interaction improves the process</li>
                    </ul>
                </div>

                <script>
                    const vscode = acquireVsCodeApi();

                    function initProject() {
                        vscode.postMessage({ type: 'init-project' });
                    }

                    function createBackup() {
                        vscode.postMessage({ type: 'create-backup' });
                    }

                    function createCheckpoint() {
                        vscode.postMessage({ type: 'create-checkpoint' });
                    }
                </script>
            </body>
            </html>
        `;
    }
}

export function deactivate() {
    console.log('FRACTAL-PROMPT extension deactivated');
}