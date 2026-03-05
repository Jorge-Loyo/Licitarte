// Template Loader - Carga templates HTML desde archivos separados
const TemplateLoader = {
    cache: {},
    
    async load(templateName) {
        if (this.cache[templateName]) {
            return this.cache[templateName];
        }
        
        try {
            const response = await fetch(`/templates/components/${templateName}.html`);
            if (!response.ok) throw new Error(`Template ${templateName} not found`);
            const html = await response.text();
            this.cache[templateName] = html;
            return html;
        } catch (error) {
            console.error(`Error loading template ${templateName}:`, error);
            return '';
        }
    },
    
    render(template, data) {
        let html = template;
        for (const [key, value] of Object.entries(data)) {
            const regex = new RegExp(`{{${key}}}`, 'g');
            html = html.replace(regex, value);
        }
        return html;
    },
    
    async loadAndRender(templateName, data) {
        const template = await this.load(templateName);
        return this.render(template, data);
    }
};
