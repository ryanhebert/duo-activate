<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />

<style type="text/css">

	.bounce-in{-webkit-animation:bouncein 1s ease-in-out;animation:bouncein 1s ease-in-out}
	@-webkit-keyframes bouncein{0%{transform:scale(.05)}
	33%{transform:scale(1.1)}
	60%{transform:scale(.96)}
	75%{transform:scale(1.03)}
	to{transform:scale(1)}
	}
	@keyframes bouncein{0%{transform:scale(.05)}
	33%{transform:scale(1.1)}
	60%{transform:scale(.96)}
	75%{transform:scale(1.03)}
	to{transform:scale(1)}
	}
	.loader{border-style:solid;border-color:#f1f3f6 #f1f3f6 #0b69e5;border-radius:50%;animation:rotate 1s ease-in-out infinite}
	.loader--size-xsmall{height:.5rem;width:.5rem;border-width:2px}
	.loader--size-small{height:.875rem;width:.875rem;border-width:2px}
	.loader--size-medium{height:2rem;width:2rem;border-width:4px}
	.loader--size-large{height:4rem;width:4rem;border-width:6px}
	.loader--size-xlarge{height:8rem;width:8rem;border-width:8px}
	.loader--size-xxlarge{height:10rem;width:10rem;border-width:10px}
	@keyframes rotate{0%{transform:rotate(180deg)}
	to{transform:rotate(540deg)}
	}
	.loader.loader--accessible{-webkit-animation:none;animation:none;display:none}
	@media screen and (prefers-reduced-motion:no-preference){.loader.loader--accessible{display:block;-webkit-animation:rotate 1s ease-in-out infinite;animation:rotate 1s ease-in-out infinite}
	}
	.loader-text{z-index:200;margin-bottom:1rem;margin-top:-6px}
	@media screen and (prefers-reduced-motion:no-preference){.loader-text{
	        /* !important tags necessary to prevent screen reader bugs... i know.. */position:absolute!important;height:1px!important;width:1px!important;overflow:hidden!important;clip:rect(1px 1px 1px 1px)!important;clip:rect(1px,1px,1px,1px)!important}
	}
</style>


<style type="text/css">
	body{
		margin: 0;
		padding: 0;
		background: #eee;
		font-family: "Helvetica Neue",Helvetica,Arial,Sans-serif;
		color: #363f44;
		height: 100%;
		width: 100%;
	}
	.app{
		border-radius: .25rem;
		width: 360px;
		background: #fff;
		overflow: hidden;
		text-align: center;
		border-top: solid 5px #7b71ff;
		box-shadow: 0 1px 2px 0 rgb(0 0 0 / 12%), 0 2px 8px 0 rgb(0 0 0 / 24%);

		position: absolute;
	    left: 50%;
	    top: 50%;
	    transform: translate(-50%,-50%);
	}

	video{
		border-radius: 125px;
		width: 250px;
		height: 250px;
		background: radial-gradient(#eee,#fff);
	}
	#start-camera{
		position: absolute;
	    left: 50%;
	    top: 50%;
	    transform: translate(-50%,-50%);

		display: block;
		padding: 0;
		margin: 0;
		border: 0;
		background: transparent;
	}
	#start-ASR{
		text-align: left;
		display: block;
		padding: 0 0 8px 0;
		margin: 0;
		border: 0;
		background: transparent;
	}
	#start-ASR:hover{
		color: #eee;
	}

	#start-record{
		display: none;
	}
	#stop-record{
		display: none;
	}
	.bars{
		margin: 0px 32px 8px 32px;
		text-align: left;
	}
	#spinny-bar-wrapper{
		text-align: center;
		margin: 24px;
		position: relative;
		height: 300px;
	}
	.spinny-bar{
		position: absolute;
	    left: 50%;
	    top: 50%;
	    transform: translate(-50%,-50%);

	    display: block;
		padding: 0;
		margin: 0;
		border: 0;
	}
	.logo-bar{
		margin-top: 32px;
		margin-bottom: 14px;
		overflow: hidden;
	}
	.desc-bar{
		font-size: 1.3em;
		font-weight: 900;
	}
	.instructions-bar{
		line-height: 1.4;
	}
	.video-bar{
		text-align: center;
		margin: 24px;
		position: relative;
		height: 250px;
	}
	.icon-bar{
		text-align: center;
		margin: 24px;
		position: relative;
	}
	.asr-bar{
		background: #eee;
		border:  solid 1px #ddd;
		border-radius: .25rem;
		font-size: 1.2em;
		padding: 8px;
		line-height: 1.5em;
		text-align: center;
	}
	.words{
		display: inline-block;
		color: #777;
		padding: 2px;
	}
	button{
		border-radius: .25rem;
		border: 0.0625rem solid #999;
		background: linear-gradient(#fff, #eee);
		color: #0b69e5;
		font-size: 1.25em;
		padding: 16px;
		width: 100%;
		margin-top: 24px;
		margin-bottom: 24px;
	}
	button:hover{
		background: linear-gradient(#0b93e5, #0b69e5);
		color: #fff;
		cursor: pointer;
	}
	button:disabled,
	button[disabled]{
		color: #ddd;
	}
	.footer-bar{
		font-size: .8em;
		margin-bottom: 32px;
		text-align: right;
	}

	#corners{
		display: block;
		border-radius: 1rem;
	    position: absolute;
	    left: 50%;
	    top: 50%;
	    transform: translate(-50%,-50%);

		background: transparent;
		border: 4px dashed rgba(221, 221, 221, .5);
		height: 160px;
		width: 160px;
	}


</style>


<style type="text/css">
	
	/* 2532x1170 pixels at 460ppi iphone 12 Pro*/
	/*@media only screen 
	    and (device-width: 390px) 
	    and (device-height: 844px) 
	    and (-webkit-device-pixel-ratio: 3) { }
	}*/

	/* any device that uses touch*/
	@media (pointer:none), (pointer:coarse) {
		body{background: black;}
		.app{width: 100%;}
	}

</style>



</head>

<body>
	<div id="app-setup" class="app">
		<div class="bars logo-bar">
			<img src="static/logo.png" height="30px" alt="Logo">
		</div>
		<div id="spinny-app-wrapper" class="app-wrapper"style="display:None;">
			<div id="spinny-bar-wrapper">
				<div class="spinny-bar" >
					<div class="loader-icon bounce-in"><div class="loader loader--size-large loader--accessible loader--push-request"></div></div>
				</div>
			</div>
		</div>
		<div id="start-app-wrapper" class="app-wrapper">
			<div class="bars desc-bar" >Get Started</div>
			<div class="bars icon-bar">
				<img src="static/cam-mic.webp" height="80px" alt="Camera and Microphone icon">
			</div>
			<div class="bars instructions-bar">
				This application will allow you to verify your identity. To continue, you must grant temporary access to the camera and microphone on your device.
			</div>
			<div class="bars submit-bar">
				<button id="grant-access-button" >Grant Access</button>
			</div>
		</div>
		<div class="bars footer-bar">Verification by WhoYou</div>
	</div>
	<div id="app-verify" class="app" style="display:None;">
		<div class="bars logo-bar">
			<img src="static/logo.png" height="30px" alt="Logo">
		</div>
		<div class="bars desc-bar">User Verification</div>
		<div class="bars video-bar bounce-in">
			<div id="corners"></div>
			<button id="start-camera" style="display:None;">Start</button>
			<button id="start-record" style="display:None;">Start Recording</button>
			<video id="video" autoplay></video>
		</div>
		<div class="bars instructions-bar">
			<button id="start-ASR" style="display:None;">Voice Verify</button>
			<button id="stop-ASR" style="display:None;"></button>
			Read the following words:
		</div>
		<div class="bars asr-bar">
			<div class="words">jeans</div>
			<div class="words">toward</div>
			<div class="words">wonder</div>
			<div class="words">emerge</div>
			<div class="words">rabbit</div>
			<div class="words">actress</div>
		</div>
		<div class="bars submit-bar">
			<button disabled="disabled" id="continue">Continue</button>
		</div>
		<div class="bars footer-bar">Verification by WhoYou</div>
	</div>
</body>

<script src="https://aka.ms/csspeech/jsbrowserpackageraw"></script>


<!-- This is the video script -->
<script type="text/javascript" defer>

let app_setup = document.querySelector("#app-setup");
let app_verify = document.querySelector("#app-verify");

let continueButton = document.querySelector("#continue");

let start_app_wrapper = document.querySelector("#start-app-wrapper");
let spinny_app_wrapper = document.querySelector("#spinny-app-wrapper");

let grant_access_button = document.querySelector("#grant-access-button");

let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let start_button = document.querySelector("#start-record");
let stop_button = document.querySelector("#stop-record");
let download_link = document.querySelector("#download-video");

let camera_stream = null;
let media_recorder = null;
let combined_stream = null;
let blobs_recorded = [];

const constraints_video = {
	    audio: false,
	    video: {
			aspectRatio: {ideal: 1}
		}
	}
const constraints_audio = {audio: true}


grant_access_button.addEventListener('click', function () {
	camera_button.click();
	start_app_wrapper.style.display = "None";
	spinny_app_wrapper.style.display = "block";

	let setup_check = setInterval(function () {
		if(combined_stream){
			console.log("setup complete");
			clearInterval(setup_check);
			app_setup.style.display = "None";
			app_verify.style.display = "block";
			startASRButton.click();
		}
	}, 1000);
});

continueButton.addEventListener('click', function () {

	app_verify.style.display = "None";
	app_setup.style.display = "block";
	let redirectTimeeout = setTimeout(function () {
		window.location.replace("http://ryan.login.duosecurity.com");
	}, 1000);
});

camera_button.addEventListener('click', async function() {

   	camera_stream = await navigator.mediaDevices.getUserMedia(constraints_video);
   	audio_stream = await navigator.mediaDevices.getUserMedia(constraints_audio);
   	combined_stream = new MediaStream([...camera_stream.getVideoTracks(), ...audio_stream.getAudioTracks()])
	
   	//show only the video stream to the end user to prevent an echo
	video.srcObject = camera_stream;

	camera_button.style.display = "None";
});

start_button.addEventListener('click', function() {
    // set MIME type of recording as video/webm
    media_recorder = new MediaRecorder(combined_stream, { mimeType: 'video/webm' });

    // event : new recorded video blob available 
    media_recorder.addEventListener('dataavailable', function(e) {
		blobs_recorded.push(e.data);
    });

    // event : recording stopped & all blobs sent
    media_recorder.addEventListener('stop', function() {
    	// create local object URL from the recorded video blobs
    	let video_local = URL.createObjectURL(new Blob(blobs_recorded, { type: 'video/webm' }));
    	download_link.href = video_local;
    });

    // start recording with each recorded blob having 1 second video
    media_recorder.start(1000);
});

/*stop_button.addEventListener('click', function() {
	media_recorder.stop(); 
});*/

</script>


<!-- This is the Azure ASR script -->






<script type="text/javascript">
	var SpeechSDK;
	var key, authorizationToken, appId, phrases;
	var remaining_words = [];
	//var regionOptions;
	//var languageOptions, formatOption, filePicker, microphoneSources;
	//var useDetailedResults;
	var recognizer;
	//var inputSourceMicrophoneRadio, inputSourceFileRadio;
	//var scenarioSelection, scenarioStartButton, scenarioStopButton;
	//var formatSimpleRadio, formatDetailedRadio;
	var reco;
	//var languageTargetOptions, voiceOutput;
	var audioFile;
	var microphoneId;
	var referenceText;
	//var pronunciationAssessmentResults;

	//var thingsToDisableDuringSession;

	var soundContext = undefined;
	try {
	    var AudioContext = window.AudioContext // our preferred impl
	        || window.webkitAudioContext       // fallback, mostly when on Safari
	        || false;                          // could not find.

	    if (AudioContext) {
	        soundContext = new AudioContext();
	    } else {
	        alert("Audio context not supported");
	    }
	} catch (e) {
	    window.console.log("no sound context found, no audio output. " + e);
	}

	document.addEventListener("DOMContentLoaded", function () {

		window.startASRButton = document.getElementById('start-ASR');
		window.stopASRButton = document.getElementById('stop-ASR');

        startASRButton.addEventListener("click", doContinuousRecognition);
        stopASRButton.addEventListener('click', function() {
        	reco.stopContinuousRecognitionAsync(
        		function () {
        			reco.close();
        			reco = undefined;
        		},
        		function (err) {
        			reco.close();
        			reco = undefined;
        		}
        	);
        });

    	window.word_divs = document.getElementsByClassName("words");

		for (let i = 0; i<word_divs.length; i++) {
			window.remaining_words.push(word_divs[i].innerHTML);
		}

		for (let i =0; i<word_divs.length; i++){
			window.phrases += word_divs[i].innerHTML + ';'
		}

		//camera_button.click();
		//startASRButton.click();
	});

  	function update_words(speech) {
  		const stop_word = "stop";
		const speech_words = speech.split(/[, ]+/);

	    for (let i = 0; i<speech_words.length; i++) {

	    	if (speech_words[i] == stop_word) {
	    		stopASRButton.click();
	    	}

	    	for (let i2 = 0; i2 < window.remaining_words.length; i2++) {

	    		let word = window.remaining_words[i2];

	    		if (speech_words[i] == word) {
	    			window.word_divs[i2].style.color = "green";
	    			window.remaining_words[i2] = null;
	    			break;
	    		}
	    	}

	    	let verified = window.remaining_words.every(element => element === null);

	    	if (verified) {
	    		onVerification();
	    	}
	    }
	}

    function applyCommonConfigurationTo(recognizer) {
        // The 'recognizing' event signals that an intermediate recognition result is received.
        // Intermediate results arrive while audio is being processed and represent the current "best guess" about
        // what's been spoken so far.
        recognizer.recognizing = onRecognizing;

        // The 'recognized' event signals that a finalized recognition result has been received. These results are
        // formed across complete utterance audio (with either silence or eof at the end) and will include
        // punctuation, capitalization, and potentially other extra details.
        // 
        // * In the case of continuous scenarios, these final results will be generated after each segment of audio
        //   with sufficient silence at the end.
        // * In the case of intent scenarios, only these final results will contain intent JSON data.
        // * Single-shot scenarios can also use a continuation on recognizeOnceAsync calls to handle this without
        //   event registration.
        recognizer.recognized = onRecognized;

        // The 'canceled' event signals that the service has stopped processing speech.
        // https://docs.microsoft.com/javascript/api/microsoft-cognitiveservices-speech-sdk/speechrecognitioncanceledeventargs?view=azure-node-latest
        // This can happen for two broad classes of reasons:
        // 1. An error was encountered.
        //    In this case, the .errorDetails property will contain a textual representation of the error.
        // 2. No additional audio is available.
        //    This is caused by the input stream being closed or reaching the end of an audio file.
        recognizer.canceled = onCanceled;

        // The 'sessionStarted' event signals that audio has begun flowing and an interaction with the service has
        // started.
        recognizer.sessionStarted = onSessionStarted;

        // The 'sessionStopped' event signals that the current interaction with the speech service has ended and
        // audio has stopped flowing.
        recognizer.sessionStopped = onSessionStopped;

        // PhraseListGrammar allows for the customization of recognizer vocabulary.
        // The semicolon-delimited list of words or phrases will be treated as additional, more likely components
        // of recognition results when applied to the recognizer.
        //
        // See https://docs.microsoft.com/azure/cognitive-services/speech-service/get-started-speech-to-text#improve-recognition-accuracy
        if (window.phrases) {
            var phraseListGrammar = SpeechSDK.PhraseListGrammar.fromRecognizer(recognizer);
            phraseListGrammar.addPhrases(window.phrases.split(";"));
        }
    }

    function doContinuousRecognition() {

    	startASRButton.disabled = true;

        var audioConfig = getAudioConfig();
        var speechConfig = getSpeechConfig(SpeechSDK.SpeechConfig);
        if (!speechConfig) return;

        // Create the SpeechRecognizer and set up common event handlers and PhraseList data
        reco = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);
        applyCommonConfigurationTo(reco);

        // Start the continuous recognition. Note that, in this continuous scenario, activity is purely event-
        // driven, as use of continuation (as is in the single-shot sample) isn't applicable when there's not a
        // single result.
        reco.startContinuousRecognitionAsync();
    }

    function getAudioConfig() {

    	return SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();

    	// Leaving other options here for reference

        // If an audio file was specified, use it. Otherwise, use the microphone.
        // Depending on browser security settings, the user may be prompted to allow microphone use. Using
        // continuous recognition allows multiple phrases to be recognized from a single use authorization.

        let use_file = false;

        if (audioFile) {
            return SpeechSDK.AudioConfig.fromWavFileInput(audioFile);
        } else if (use_file) {
            alert('Please choose a file when selecting file input as your audio source.');
            return;
        } else if (microphoneSources.value) {
            return SpeechSDK.AudioConfig.fromMicrophoneInput(microphoneSources.value);
        } else {
            return SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
        }
    }

    function getSpeechConfig(sdkConfigType) {
    	const key = "0507432a234a4a45a13f478edbe634b1";
    	const regionOptions = "eastus";
        var speechConfig;
        if (authorizationToken) {
            speechConfig = sdkConfigType.fromAuthorizationToken(key, regionOptions);
        } else if (!key) {
            alert("Please enter your Cognitive Services Speech subscription key!");
            return undefined;
        } else {
            speechConfig = sdkConfigType.fromSubscription(key, regionOptions);
        }

        let use_detailed = false;
        if(use_detailed){
        	speechConfig.outputFormat = SpeechSDK.OutputFormat.Detailed;
        }

        return speechConfig;
    }

/*    function getPronunciationAssessmentConfig() {
        var pronunciationAssessmentConfig = new SpeechSDK.PronunciationAssessmentConfig(referenceText,
            SpeechSDK.PronunciationAssessmentGradingSystem.HundredMark,
            SpeechSDK.PronunciationAssessmentGranularity.Word, true);
        return pronunciationAssessmentConfig;
    }*/

    function onRecognizing(sender, recognitionEventArgs) {
        var result = recognitionEventArgs.result;

        //Ryan Start

        update_words(result.text);

        //Ryan Stop


        statusDiv.innerHTML += `(recognizing) Reason: ${SpeechSDK.ResultReason[result.reason]}`
            + ` Text: ${result.text}\r\n`;
        // Update the hypothesis line in the phrase/result view (only have one)
        phraseDiv.innerHTML = phraseDiv.innerHTML.replace(/(.*)(^|[\r\n]+).*\[\.\.\.\][\r\n]+/, '$1$2')
            + `${result.text} [...]\r\n`;
        phraseDiv.scrollTop = phraseDiv.scrollHeight;
    }

    function onRecognized(sender, recognitionEventArgs) {
        var result = recognitionEventArgs.result;
        onRecognizedResult(recognitionEventArgs.result);
        console.log("onRecognized");
    }

    function onSessionStarted(sender, sessionEventArgs) {
        window.console.log('(sessionStarted) SessionId: ' + sessionEventArgs.sessionId);

        let sessionTimeoutSeconds = 30;
        console.log('Session will timeout in ' + sessionTimeoutSeconds + ' seconds.');
        window.sessionTimeout = setTimeout(function () {
        	alert("Verification has timed out. Please refresh the page to try again.");
        	stopASRButton.click();
        }, sessionTimeoutSeconds*1000);

    }

    function onSessionStopped(sender, sessionEventArgs) {
        window.console.log('(sessionStopped) SessionId: ' + sessionEventArgs.sessionId);
        clearTimeout(window.sessionTimeout);
        //startASRButton.disabled = false;
    }

    function onCanceled (sender, cancellationEventArgs) {
        window.console.log(e);
        clearTimeout(window.sessionTimeout);
    }

    function onVerification () {
    	window.console.log("verified");
    	stopASRButton.click();
    	continueButton.disabled = false;
    	startASRButton.disabled = true;
    }

</script>
