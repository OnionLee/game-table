using UnityEngine;
using UnityEditor;

public class TablePostprocessor : AssetPostprocessor 
{	
	private static void OnPostprocessAllAssets (string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths) 
	{
		foreach (string str in importedAssets)
		{
			if (str.EndsWith(".xlsx"))
				Convert ();
		}
	}

	private static void Convert()
	{
		Debug.Log ("TODO : Auto Convert");
	}
}