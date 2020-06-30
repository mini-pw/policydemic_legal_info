const Koa = require('koa');
const KoaRouter = require('koa-router');
const bodyParser = require('koa-bodyparser');
const multer = require('koa-multer');
const cors = require('@koa/cors');

const app = new Koa();
const router = new KoaRouter();
const upload = multer();

router.get('/', (ctx) => {
  ctx.body = "Hello world!"
})

router.get('/autocomplete/websites', (ctx) => {
  ctx.body = JSON.stringify([
    {name: 'google.com', value: 'google.com'},
    {name: 'bing.com', value: 'bing.com'},
  ])
})

router.get('/autocomplete/countries', (ctx) => {
  ctx.body = JSON.stringify([
    {name: "Poland", value: "Poland"},
    {name: "USA", value: "USA"},
    {name: "China", value: "China"},
    {name: "Italy", value: "Italy"},
  ])
})

router.get('/autocomplete/languages', (ctx) => {
  ctx.body = JSON.stringify([
    {name: "Polish", value: "Polish"},
    {name: "English", value: "English"},
    {name: "Chinese", value: "Chinese"},
    {name: "Italian", value: "Italian"},
  ])
})

router.get('/autocomplete/keywords', (ctx) => {
  ctx.body = JSON.stringify([
    {name: "School Closing", value: "School Closing"},
    {name: "Shopping restrictions", value: "Shopping restrictions"},
  ])
})

router.get('/autocomplete/translationTypes', (ctx) => {
  ctx.body = JSON.stringify([
    {name: "none", value: "none"},
    {name: "Google Translate", value: "Google Translate"},
    {name: "DeepL", value: "DeepL"},
  ])
})

router.get('/documents/:id', (ctx) => {
  console.log(ctx.params.id);
  
  ctx.body = JSON.stringify({
      webPage: "web page",
      organization: "organization",
      section: "section",
      keywords: ["School Closing", "Shopping restrictions"],
      infoDate: new Date(2020, 3, 1),
      scrapDate: new Date(2020, 4, 1),
      country: "Poland",
      language: "Polish",
      translationType: "Google Translate",
      translation: "translation",
      originalText: "translation",
  })
})


router.get('/', (ctx) => {
  ctx.body = "Hello world!"
})

router.get('/', (ctx) => {
  ctx.body = "Hello world!"
})

router.post('/lad', upload.single('pdf'), (ctx) => {
  console.log(ctx.request)
  console.log(ctx.req.body)
  console.log('ctx.req.file', ctx.req.file);

  ctx.status = 200
});

router.post('/ssd', upload.single('pdf'), (ctx) => {
  console.log(ctx.request)
  console.log(ctx.req.body)

  ctx.status = 200
});

router.post('/crawler/saveConfig', (ctx) => {
  console.log(ctx.request)
  console.log(ctx.request.body)

  ctx.status = 200
});

router.post('/crawler/run', (ctx) => {
  console.log(ctx.request)
  console.log(ctx.request.body)

  ctx.status = 200
});

app
  .use(cors())
  .use(bodyParser())
  .use(router.routes())
  .use(router.allowedMethods());

app.listen(8000);