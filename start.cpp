#include <windows.h>
#include <bits/stdc++.h>
using namespace std;

bool RunCommandNoWindow(const string& command) {
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    ZeroMemory(&pi, sizeof(pi));

    // 设置窗口不可见
    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;

    // 创建进程
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

    // 等待进程结束
    WaitForSingleObject(pi.hProcess, INFINITE);

    // 关闭句柄
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return true;
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
    RunCommandNoWindow("pythonw.exe PortablePython.pyw");

    return 0;
}
