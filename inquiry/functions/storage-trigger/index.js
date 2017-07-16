/**
 * Copyright 2016, Google, Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

const Buffer = require('safe-buffer').Buffer;

// [START functions_pubsub_setup]
const PubSub = require('@google-cloud/pubsub');

// Instantiates a client
const pubsub = PubSub();
// [END functions_pubsub_setup]

// [START functions_helloworld_debug]
require('@google-cloud/debug-agent').start();
// [END functions_helloworld_debug]

// [START functions_helloworld_storage]
/**
 * Background Cloud Function to be triggered by Cloud Storage.
 *
 * @param {object} event The Cloud Functions event.
 * @param {function} callback The callback function.
 */
exports.GCStoPubSub = function (event, callback) {
  const file = event.data;

  if (file.resourceState === 'not_exists') {
    console.log(`File ${file.name} deleted.`);
  } else if (file.metageneration === '1') {
    // metageneration attribute is updated on metadata changes.
    // on create value is 1
    console.log(`File ${file.name} uploaded.`);
  } else {
    console.log(`File ${file.name} metadata updated.`);
  }

  const topic_name = 'jbei-sync-notify-topic';
  const topic = pubsub.topic(topic_name);
  console.log(`Publishing message to topic ${topic}`);

  const message = {
    data: {
      message: `File ${file.name} changed.`
    }
  };

  // Publishes a message
  return topic.publish(message)
    .then(() => res.status(200).send('Message published.'))
    .catch((err) => {
      console.error(err);
      res.status(500).send(err);
      return Promise.reject(err);
    });

  callback();
};
// [END functions_helloworld_storage]

// [START functions_pubsub_subscribe]
/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {object} event The Cloud Functions event.
 * @param {object} event.data The Cloud Pub/Sub Message object.
 * @param {string} event.data.data The "data" property of the Cloud Pub/Sub Message.
 * @param {function} The callback function.
 */
exports.subscribe = function subscribe (event, callback) {
  const pubsubMessage = event.data;

  // We're just going to log the message to prove that it worked!
  console.log(Buffer.from(pubsubMessage.data, 'base64').toString());

  // Don't forget to call the callback!
  callback();
};
// [END functions_pubsub_subscribe]

// [START functions_helloworld_error]
/**
 * Background Cloud Function that throws an error.
 *
 * @param {object} event The Cloud Functions event.
 * @param {function} callback The callback function.
 */
exports.helloError = function helloError (event, callback) {
  // This WILL be reported to Stackdriver errors
  throw new Error('I failed you');
};
// [END functions_helloworld_error]

/* eslint-disable */
// [START functions_helloworld_error_2]
/**
 * Background Cloud Function that throws a value.
 *
 * @param {object} event The Cloud Functions event.
 * @param {function} callback The callback function.
 */
exports.helloError2 = function helloError2 (event, callback) {
  // This will NOT be reported to Stackdriver errors
  throw 1;
};
// [END functions_helloworld_error_2]

// [START functions_helloworld_error_3]
/**
 * Background Cloud Function that throws an error.
 *
 * @param {object} event The Cloud Functions event.
 * @param {function} callback The callback function.
 */
exports.helloError3 = function helloError3 (event, callback) {
  // This will NOT be reported to Stackdriver errors
  callback('I failed you');
};
// [END functions_helloworld_error_3]
/* eslint-enable */

// [START functions_helloworld_template]
const path = require('path');
const pug = require('pug');

// Renders the index.pug
exports.helloTemplate = (req, res) => {
  // Render the index.pug file
  const html = pug.renderFile(path.join(__dirname, 'index.pug'));

  res.send(html).end();
};
// [END functions_helloworld_template]
