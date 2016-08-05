using System;
using System.Collections.ObjectModel;
using Newtonsoft.Json;

public class CharacterDescriptor : BaseDescriptor
{
	[JsonProperty("name")]
	public string Name {get; private set;}

	[JsonProperty("Child")]
	public ReadOnlyCollection<ChildDescriptor> Childs {get; private set;}
}

public class ChildDescriptor : BaseDescriptor
{
	[JsonProperty("name")]
	public string Name {get; private set;}

	[JsonProperty("power")]
	public float Power {get; private set;}

	[JsonProperty("ChildChild")]
	public ReadOnlyCollection<ChildChildDescriptor> ChildChilds {get; private set;}
}

public class ChildChildDescriptor : BaseDescriptor
{
	[JsonProperty("name")]
	public string Name {get; private set;}

	[JsonProperty("power")]
	public float Power {get; private set;}
}