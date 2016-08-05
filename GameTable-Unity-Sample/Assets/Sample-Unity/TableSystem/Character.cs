using System;
using UnityEngine;

public class Character : MonoBehaviour
{
	[SerializeField]
	private string id;

	private CharacterDescriptor desc;

	private void Awake()
	{
		desc = TableLocator.CharacterTable.Find (id);
		Debug.Log (desc.Name);
		Debug.Log (desc.Id);
	}
}

