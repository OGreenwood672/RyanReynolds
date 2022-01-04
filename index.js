const Discord = require("discord.js");
const jsondata = require('./quizzes.json'); 
require("dotenv").config();

const token = process.env.TOKEN;

const client = new Discord.Client({ intents: [Discord.Intents.FLAGS.GUILDS, Discord.Intents.FLAGS.GUILD_MESSAGES] });

const prefix = "revise ";

var questions = [];
var ans = "";

client.once("ready", () => {
  console.log("Ready!");
});

client.once("reconnecting", () => {
  console.log("Reconnecting!");
});

client.once("disconnect", () => {
  console.log("Disconnect!");
});

client.on("messageCreate", async message => {

	if (!message.content.startsWith(prefix)) return;

	if (message.content.startsWith(`${prefix}list`)) {

		message.channel.send(Object.keys(jsondata).join("\n"));


	} else if (message.content.startsWith(`${prefix}use`)) {

		use( message )

	} else if (message.content.startsWith(`${prefix}next`)) {

		if (questions.length == 0) {
			message.channel.send("No questions queued");
		} else {
			next( message );
		}

	} else if (message.content.startsWith(`${prefix}answer`)) {

		answer( message );

	} else {
		message.channel.send("You need to enter a valid command!");
	}
});

function use(message) {
	const args = message.content.split(" ");

	args.splice(0, 2);
	let title = args.join(" ")


	if (jsondata[title] == undefined) {

		message.channel.send("No topic found by that name");

	} else {

		questions = jsondata[title];
		message.channel.send(`${title} has been loaded`);

	}


}

function next( message ) {

	var index = Math.floor(Math.random() * questions.length);

	message.channel.send("Question: " + questions[index][0]);
	ans = questions[index][1];

	questions.splice(index, 1);

}

function answer( message ) {

	if (ans.length > 0) {
		message.channel.send("Answer: " + ans);
	} else {
		message.channel.send("No answer found")
	}

}

client.login(token);