using System.Diagnostics;
using UnityEditor;
using UnityEngine;
using System.Linq;

public class TablePostProcessor : AssetPostprocessor
{
    //Edit this fields

    //Excel, Generator Path
    private static string kRootPath = "/GameTable-Generator";
    private static string kGeneratorFileName = "generator.py";
    private static string kJsonPath = "/Sample/Resources/Table/";

    private static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths)
    {
        foreach (string filePath in importedAssets)
        {
            if (filePath.Contains(kRootPath) == false)
                continue;

            // Check is this Excel file
            if (filePath.EndsWith(".xlsx") == false)
                continue;

            // Check is this temp file
            if (filePath.StartsWith("~"))
                continue;

            Generate();
            break;
        }
    }

    private static void Generate()
    {
        RunGenerator();

        AssetDatabase.Refresh();
    }

    private static void RunGenerator()
    {
        var cmdPath = Application.dataPath + kJsonPath;
        cmdPath.Replace(@"\", @"/");

        var proInfo = new ProcessStartInfo();
        proInfo.FileName = @"py";
        proInfo.WorkingDirectory = Application.dataPath + kRootPath;
        proInfo.Arguments = kGeneratorFileName + " " + cmdPath;

        proInfo.CreateNoWindow = true;
        proInfo.UseShellExecute = false;

        proInfo.RedirectStandardOutput = true;
        proInfo.RedirectStandardError = true;

        var pro = new Process();
        pro.StartInfo = proInfo;
        pro.Start();

        var logs = pro.StandardOutput.ReadToEnd().Split('\n').Where(l => l.Length > 0 && l[0] != '\r').Skip(0);
        pro.WaitForExit();
        pro.Close();

        foreach (var log in logs)
        {
            if (log.Contains("[error]"))
            {
                UnityEngine.Debug.LogError(log);
            }
            else
            {
                UnityEngine.Debug.Log(log);
            }
        }
    }
}