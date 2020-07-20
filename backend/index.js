const Koa = require('koa');
const KoaRouter = require('koa-router');
const bodyParser = require('koa-bodyparser');
const multer = require('koa-multer');
const cors = require('@koa/cors');
const { Client } = require('@elastic/elasticsearch')
const client = new Client({node: 'http:/localhost:9200'})


const app = new Koa();
const router = new KoaRouter();
const upload = multer();


router.get('/', (ctx) => {
  ctx.body = "Hello world!"
})

router.get('/autocomplete/webpages', (ctx) => {
  ctx.body = JSON.stringify([
      {name: 'google.com', value: 'google.com'},
      {name: 'test', value: 'test_webpage.com'},
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

router.get('/populate', (ctx) => {
    populate().then(r => console.log(r)).catch(console.log)
    ctx.status = 200
})
async function populate (){

    await client.index({
        index: 'documents',
        body:{
                web_page: 'test_webpage23.com',
                document_type: 'legalact',
                pdf_path: 'test_path',
                scrap_date: '2020-10-23 10:00:00',
                info_date: '2020-12-12',
                country: "Poland",
                language: "Polish",
                translation_type: "automatic",
                text_parsing_type: "ocr",
                keywords: ["test_kw"],
                original_text: "Oryginalny tekst dokumentu",
                translated_text: "Original text of the document",
                organization: "Test1",
                section: null
        }
    })
        .catch(e => {
            console.log(e)
        });

    await client.index({
        index: 'documents',
        body:{
            web_page: 'test_webpage.gov.pl',
            document_type: 'secondary',
            pdf_path: 'test_path',
            scrap_date: '2020-10-05 10:00:00',
            info_date: '2020-12-15',
            country: "Poland",
            language: "Polish",
            translation_type: "automatic",
            text_parsing_type: "ocr",
            keywords: ["si", "certo", "torro"],
            original_text: "Oryginalny tekst dokumentu",
            translated_text: "Original text of the document",
            organization: "Test2",
            section: null
        }
    })
        .catch(e => {
            console.log(e)
        });

    await client.index({
        index: 'documents',
        body:{
            web_page: 'test_webpageDE.com',
            document_type: 'legalact',
            pdf_path: 'test_path',
            scrap_date: '2020-11-23 10:00:00',
            info_date: '2020-07-12',
            country: "Germany",
            language: "German",
            translation_type: "manual",
            text_parsing_type: "parser",
            keywords: ["covid", "bulk"],
            original_text: "Oryginalny tekst dokumentu",
            organization: "Test3",
            translated_text: "Original text of the document",
            section: null
        }
    })
        .catch(e => {
            console.log(e)
        });

    await client.index({
        index: 'documents',
        body:{
            web_page: 'italian.gov.com',
            document_type: 'secondary',
            pdf_path: 'test_path',
            scrap_date: '2020-01-23 10:00:00',
            info_date: '2020-02-12',
            country: "Italy",
            language: "Italian",
            translation_type: "automatic",
            text_parsing_type: "ocr",
            keywords: ["testIT", "pizza", "espresso"],
            original_text: "Oryginalny tekst dokumentu",
            organization: "Test1",
            translated_text: "Original text of the document",
            section: null
        }
    })
        .catch(e => {
            console.log(e)
        });

    await client.index({
        index: 'documents',
        body:{
            web_page: 'test_webpage23.com',
            document_type: 'secondary',
            pdf_path: 'test_path',
            scrap_date: '2020-10-23 10:00:00',
            info_date: '2020-12-12',
            country: "Poland",
            language: "Polish",
            translation_type: "automatic",
            text_parsing_type: "ocr",
            keywords: "test_kw",
            original_text: "Oryginalny tekst dokumentu",
            organization: "Test2",
            translated_text: "Original text of the document",
            section: null
        }
    })
        .catch(e => {
            console.log(e)
        });



    await client.indices.refresh({
        index: 'documents'
    })
}
async function getDocuments(ctx, documentType) {
    const data = await fetchDocumentsFromElastic(ctx.request.body, documentType)
        .catch(console.log)
        .then(resp => {
            ctx.body = parseData(resp);
            ctx.status = 200
        }, error => {
            console.log("Error " + error)
        })
}

router.post('/ssd/search', async (ctx) => {
    console.log(ctx.request.body)
    await getDocuments(ctx, "secondary");
});


function parseData(data){
    const parsedData = [];
    data.forEach(element => {
        parsedData.push({
            id: element._id,
            source: element._source.organization,
            infoDate: element._source.info_date,
            language: element._source.language,
            keywords: element._source.keywords,
            country: element._source.country
        })
    });
    return parsedData;
}
async function fetchDocumentsFromElastic(body, documentType){
    let params = constructParams(body, documentType)
    let request = await client.search(params);
    return  request.body.hits.hits;
}
function constructParams(body, documentType){
    let params = {
        index: 'documents',
        body: {
            query:{
                bool: {
                    must: [
                        { match: { document_type: documentType}}],
                }
            }
        }
    }

    if(body.infoDateTo.length > 0 && body.infoDateFrom.length > 0){
        params.body.query.bool.must.push({ range: { info_date: { gte: body.infoDateFrom, lte: body.infoDateTo }}},)
    }

    let fields = ["web_page", "country", "language", "keywords" ];

    for(let i = 0; i < fields.length; i++){

        if (body[fields[i]].length > 0) {
            let boolStatement = {
                bool: {
                    should: []
                }
            };
            for( let j=0; j<body[fields[i]].length; j++) {

                let matchStatement = {
                    match: ""
                };
                let fieldStatement = {};

                fieldStatement[fields[i]] = body[fields[i]][j]
                matchStatement["match"] = fieldStatement
                boolStatement.bool.should.push(matchStatement)
            }

            params.body.query.bool.must.push(boolStatement)
            }
        }

    console.log(JSON.stringify(params))
    return params
}


router.post('/lad/search', async (ctx) => {
    console.log(ctx.request)
    await getDocuments(ctx, "legalact");
});



module.exports = constructParams;
app
  .use(cors())
  .use(bodyParser())
  .use(router.routes())
  .use(router.allowedMethods());

app.listen(8000);