using UnityEngine;
using UnityEditor;
using System.Diagnostics;

public class TablePostprocessor : AssetPostprocessor 
{
	//Edit script path
	private static string scriptPath = "/Sample-Unity/TableSystem/Excel/convert.py";
	private static void OnPostprocessAllAssets (string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths) 
	{
		foreach (string str in importedAssets)
		{
			if (str.Contains (".xlsx"))
				Convert ();
		}
	}

	private static void Convert()
	{
		Process.Start (Application.dataPath + scriptPath);
		UnityEngine.Debug.Log ("Convert");
	}
}