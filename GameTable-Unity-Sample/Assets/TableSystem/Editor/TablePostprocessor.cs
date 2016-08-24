using UnityEngine;
using UnityEditor;

using System.Collections.Generic;
using System.Diagnostics;


public class TablePostProcessor : AssetPostprocessor 
{
	// Full path to the Asset
	static string FullPathToExcel = Application.dataPath + "/GameTable-AutomaticConverter/Editor/Excel/";

	// Excel file Improt path
	static string ExcelPath = null;

	// Python script path
	static string ConverterPath = Application.dataPath + "/GameTable-AutomaticConverter/Editor/Automatic Converter.lnk";

	static bool isInitialize = false;

	private static void Initialize()
	{
		string[] splitPath = FullPathToExcel.Split('/');

		// Assets/GameTable-AutomaticConverter/Editor/Excel/ - 4 form behind
		ExcelPath =	splitPath[splitPath.Length - 5] + "/" +
					splitPath[splitPath.Length - 4] + "/" +
					splitPath[splitPath.Length - 3] + "/" +
					splitPath[splitPath.Length - 2] + "/";

		isInitialize = true;
	}

	private static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths) 
	{
		if(isInitialize == false)
			Initialize();

		// Imported Asset
		foreach (string filePath in importedAssets)
		{
			// Check is this temp file
			if (filePath.StartsWith("~"))
				continue;

			// Check is this Excel file
			if (filePath.EndsWith(".xlsx") == false)
				continue;

			// Check is this in ExcelPath
			if (filePath.StartsWith(ExcelPath))
				Convert();
		}
	}

	private static void Convert()
	{
		UnityEngine.Debug.Log("Excecute Automatic Cconvert");
		ConvertExcelToJson();
	}

	private static void ConvertExcelToJson()
	{
		Process.Start(ConverterPath, "");
	}

	public static void TempConvertExcelToJson()
	{
		Process process = new Process();
		process.StartInfo.FileName = ConverterPath;
		process.StartInfo.Arguments = "";

		// Pipe the output to itself - we will catch thawdis later
		process.StartInfo.RedirectStandardError = true;
		process.StartInfo.RedirectStandardOutput = true;
		process.StartInfo.CreateNoWindow = true;

		// Where the script lives
		process.StartInfo.WorkingDirectory = Application.dataPath + "/TableSystem/GameTable-AutomaticConverter/Editor/Program/";
		process.StartInfo.UseShellExecute = false;

		process.Start();

		// Read the output - this will show is a single entry in the console - you could get  fancy and make it log for each line - but thats not why we're here
		UnityEngine.Debug.Log(process.StandardOutput.ReadToEnd());
		process.WaitForExit();
		process.Close();	
	}
}

