





NullAesthetica is a [Prosthetic](http://developer.weavrs.com/) for [Weavrs](http://weavrs.com/) that posts New Aesthetic assembages ideas to your Weavrs' publishing stream.

# Installation

NullAesthetica uses the prosthetic-runner system to run on Google App Engine.

You can download prosthetic-runner [here](https://github.com/philterphactory/prosthetic-runner), along with instructions on how to install a Prosthetic such as this one into it. Particularly see the section "Adding a prosthetic to the server" newar the bottom of the page.

You will need to add this entry to index.yaml:

 - kind: nullaesthetica_config
   properties:
   - name: __key__
   direction: desc

Once you have prosthetic-runner and this Prosthetic installed, you can attach this Prosthetic to your Weavrs.
