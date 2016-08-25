using UnityEngine;
using UnityEditor;

using System.Collections.Generic;
using System.Diagnostics;


public class TablePostProcessor : AssetPostprocessor 
{
	//Edit this field
	//Excel File Path
	static string kExcelFilesPath = "/Sample/Excel";

	//Edit this field
	//Converter Path
	static string kConverterPath = "/Sample/run.bat";

	private static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths) 
	{
		foreach (string filePath in importedAssets)
		{
			if (filePath.Contains (kExcelFilesPath) == false)
				continue;

			// Check is this Excel file
			if (filePath.EndsWith(".xlsx") == false)
				continue;
			
			// Check is this temp file
			if (filePath.StartsWith("~"))
				continue;

			Convert ();
		}
	}

	private static void Convert()
	{
		// Logging
		UnityEngine.Debug.Log("Excecute Automatic Cconvert");

		// Convert
		ConvertExcelToJson();

		// Refresh Assets folder
		AssetDatabase.Refresh();
	}

	private static void ConvertExcelToJson()
	{
		UnityEngine.Debug.Log (Application.dataPath + kConverterPath);
		Process.Start(Application.dataPath + kConverterPath, "").WaitForExit();
	}
}