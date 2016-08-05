using UnityEngine;
using System.Collections;

public static class TableLocator 
{
	public static CharacterTable CharacterTable { get; private set; }

	static TableLocator()
	{
		CharacterTable = new CharacterTable ("Table/Character");
	}
}
