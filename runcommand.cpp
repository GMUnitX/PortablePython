#include <windows.h>
#include <bits/stdc++.h>
using namespace std;

int main() {
	HWND hWnd = GetConsoleWindow();
	ShowWindow(hWnd, SW_HIDE);
	
	// 获取当前工作目录
    char buffer[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, buffer);

    // 设置环境变量名称
    const char* envVarName = "PATH";
    
    // 设置当前进程环境变量（立即生效）
    SetEnvironmentVariableA(envVarName, buffer);
    
	system("cmd");

    return 0;
}
