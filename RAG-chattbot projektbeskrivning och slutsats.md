**Problem och behov**



More Sailings e-learning innehåller stora mängder information i form av utbildningsmaterial, rutiner och instruktioner. För användare, exempelvis säsongspersonal eller instruktörer, kan det vara tidskrävande att hitta rätt information när de behöver den. Detta kan leda till ineffektivitet, missförstånd, eller att viktig information inte används i praktiken.



Behovet är därför en lösning som snabbt och enkelt kan besvara frågor baserat på det befintliga utbildningsmaterialet. Lösningen ska fungera som ett stöd i det dagliga arbetet och minska behovet av att manuellt söka igenom dokument.



Målet är att utveckla en AI-baserad chattbot som använder RAG för att hämta relevant information från e-learning-materialet och generera korrekta och kontextbaserade svar. Lösningen ska vara enkel att använda och kunna testas som en prototyp.



**Scope och avgränsningar**



För att möjliggöra en fungerande prototyp inom projektets tidsram avgränsas lösningen enligt följande:



\- Endast textbaserat material från e-learningen används.

\- Datainsamling sker manuellt med API och ingen automatisk uppdatering implementeras i detta skede.

\- Ingen användarhantering eller autentisering implementeras.

\- Fokus ligger på att demonstrera funktionaliteten i en RAG-lösning, inte på färdig produkt eller frontend.

\- Inte heller alla kurser kommer att användas utan bara 11 utvalda.



Dessa avgränsningar gör det möjligt att snabbt utveckla och testa en första version. Vid vidare utveckling skulle lösningen kunna utökas med exempelvis API-integration, större datamängder och förbättrad användarupplevelse, men också bättre prestanda.



**Genomförande och lösning**



För att möta det identifierade behovet har en prototyp av en AI-baserad chattbot utvecklats med hjälp av RAG. Lösningen bygger på att kombinera informationssökning i befintligt kursmaterial med en språkmodell som genererar svar baserat på relevant kontext.



Arbetet har genomförts i flera steg. Först har utbildningsmaterial från e-learningen samlats in och bearbetats till strukturerade JSON-filer. Därefter har materialet delats upp i mindre delar (chunks) för att möjliggöra effektiv sökning. Dessa textdelar har sedan omvandlats till embeddings och lagrats i en Vector Store.



När en användare ställer en fråga omvandlas frågan till en embedding och jämförs med det lagrade materialet för att hitta de mest relevanta textdelarna. Dessa skickas tillsammans med frågan till en språkmodell som genererar ett svar baserat på den hämtade kontexten.



För att säkerställa att lösningen når upp till uppsatta mål har enklare tester och en evaluering genomförts där modellens svar jämförts med förväntade svar. Detta har gjort det möjligt att identifiera förbättringsområden, exempelvis hur materialet delas upp i chunks och hur prompten utformas.



I flera fall visade testerna att relevant information fanns i de hämtade textstyckena, men att modellen ändå inte gav rätt svar. Detta indikerar att problemet inte enbart ligger i retrieval steget, utan även i hur informationen är strukturerad. Framför allt bidrar större chunks till ökat brus, vilket gör det svårare för modellen att förstå vad som är relevant för frågan.



Lösningen visar hur AI kan användas för att göra stora mängder ostrukturerad information mer tillgänglig och användbar i praktiken. Samtidigt finns begränsningar, såsom beroende av datakvalitet och risken för felaktiga eller ofullständiga svar, vilket är viktiga insikter att ta med sig vid vidare utveckling.



**Begränsningar och vidare utveckling**



Den nuvarande lösningen är en prototyp vilket innebär vissa begränsningar. En viktig aspekt är att samma chunking logik används för allt kursmaterial där en logik för att få så jämna chunks som möjligt prioriterats, trots att innehållet skiljer sig väldigt mycket mellan olika kurser. Detta gjordes för att spara tid till bekostnad av precision i retrieval. I en mer avancerad lösning hade det varit mer effektivt att anpassa chunking logiken per kurs eller innehållstyp för att minska brus och förbättra träffsäkerheten i retrieval steget.



Lösningen bygger på en RAG och prompt, vilket fungerar bra för generella frågor men kan vara sämre för specifika områden, exempelvis frågor om destinationer. En möjlig vidareutveckling hade därför varit att använda flera separata RAG lösningar eller specialiserade prompts beroende på frågetyp, för att öka precisionen i svaren.



En annan begränsning är att chattboten saknar minne. Den behandlar varje fråga isolerat och kan inte ta hänsyn till tidigare interaktioner. I en verklig implementation hade det varit värdefullt att införa någon form av konversationsminne, där modellen kan komma ihåg tidigare frågor och anpassa svaren utifrån användarens behov.



Sammanfattningsvis finns det potential i att vidareutveckla lösningen genom mer kontextanpassad preprocessing, mer specialiserade RAG-strukturer och även förbättrad hantering av användarkontext.





