#include <windows.h>
#include <bits/stdc++.h>
using namespace std;

bool RunCommandNoWindow(const string& command) {
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    ZeroMemory(&pi, sizeof(pi));

    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;

    CreateProcessA(
        nullptr,
        const_cast<char*>(command.c_str()),
        nullptr,
        nullptr,
        FALSE,
        CREATE_NO_WINDOW,
        nullptr,
        nullptr,
        &si,
        &pi);

    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return true;
}

string ReadFileToString(const string& filename) {
    ifstream file(filename, ios::binary);
    return string((istreambuf_iterator<char>(file)),
                  istreambuf_iterator<char>());
}

int main() {
    HWND hWnd = GetConsoleWindow();
    ShowWindow(hWnd, SW_HIDE);
    
    // 获取当前工作目录
    char buffer[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, buffer); 
    // 设置环境变量名称
    const char* envVarName = "PATH";
    
    //设置当前进程环境变量（立即生效）
    SetEnvironmentVariableA(envVarName, buffer);

    string fileToRun = ReadFileToString("startfile.txt");
    fileToRun.erase(fileToRun.find_last_not_of(" \r\n") + 1);

    string pythonExe;
    if (fileToRun.size() >= 4 && fileToRun.substr(fileToRun.size() - 4) == ".pyw") {
        pythonExe = "pythonw.exe";
    } else {
        pythonExe = "python.exe";
    }

    string command = pythonExe + " \"" + fileToRun + "\"";
    RunCommandNoWindow(command);

    return 0;
}
