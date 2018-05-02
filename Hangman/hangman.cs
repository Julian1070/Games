using System;
using System.Collections.Generic;

namespace hangman
{
	class MainClass
	{
		public static void Main(string[] args)
		{

			string solution = "chair";
			Console.WriteLine("Let's play 'Hangman'! Guess a word with " + solution.Length + " letters.");
		Guess:
			string check = "";
			string word = Console.ReadLine();
			if (word.Length != solution.Length)
			{
				Console.WriteLine("Only " + solution.Length + "-letter words... try again:");
				goto Guess;
			}
			for (int i = 0; i < solution.Length; i = i + 1)
			{
				if (word[i] == solution[i])
				{
					check = check + "✓";
				}
				else check = check + "✗";
			}
			Console.WriteLine(check);
			if (word == solution)
			{
				Console.WriteLine("Congrats! You got it right!");
			}
			goto Guess;
		}
	}
}
