const express = require('express');
const request = require('request');
const cors = require('cors')
const app = express();
require('dotenv').config()

app.use(cors())
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  // res.header()
  next();
});


// ==========================================================

// const {TwitterApi} = require('twitter-api-v2');
//
// const client = new TwitterApi({
//
// });

// Instanciate with desired auth type (here's Bearer v2 auth)
// const twitterClient = new TwitterApi('AAAAAAAAAAAZFJOfG8cMdgkEJ3fSpdHN2qB%2TxBIJBRqa1n0YgeuaZfPLN');
// const roClient = twitterClient.readOnly;

// var url1 = "https://api.twitter.com/2/users/by/username/";
// var url2 = req.params.tagId;
// var url3 = "?user.fields=created_at,description,entities,id,location,name,profile_image_url,protected,url,username,verified,created_at,id";
// var url = url1.concat(url2,url3)
// console.log(url)
//
// var access_token = "AAAAAAAAAAApagEAAAABMdgkEJ3fSKzeiE2U4lRqa1nOfG8cHN2qpd0YgeuaZfPLN"
// // const user = await roClient.v2.userByUsername('TwitterDev');
// request( url ,{
  //   method: 'POST',
  //   dataType: 'json',
  //   headers :{
    //       Authorization:"Bearer " + access_token // token
    //   }
    // },
    //   (response, res, resagain) => {
      //     console.log("third" , resagain)
      //   }
      // )
      //
      // res.send(url)


// ===========================================================

const needle = require('needle');
const token = process.env.BEARER_TOKEN;
const endpointURL = "https://api.twitter.com/2/users/by?usernames="

async function getRequest() {

    const params = {
        usernames: "TwitterDev", // Edit usernames to look up
        "user.fields": "followers_count,friends_count,listed_count,favourites_count,statuses_count", // Edit optional query parameters here
        "expansions": "pinned_tweet_id"
    }

    const res = await needle('get', endpointURL, params, {
        headers: {
            "User-Agent": "v2UserLookupJS",
            "authorization": `Bearer ${token}`
        }
    })

    if (res.body) {

          request.post({url:'http://localhost:8000/scoreJson', formData: {"heelo":"okay"}}, function optionalCallback(err, httpResponse, body) {
            if (err) {
              return console.error("8000 Fail");
            }
            console.log("8000 Pass" , body);
          });

        return res.body;
    } else {
        throw new Error('Unsuccessful request')
    }

}



app.get('/:tagId', async (req, res) => {



      try {
          const response = await getRequest();
          console.dir(response, {
              depth: null
          });

      } catch (e) {
          console.log(e);

      }

      res.send("Request Complete, please check console")

});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`listening on ${PORT}`));
