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

app
  .use(cors())
  .use(bodyParser())
  .use(router.routes())
  .use(router.allowedMethods());

app.listen(8000);