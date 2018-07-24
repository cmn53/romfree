L.Icon.Glyph = L.Icon.extend({
	options: {
		iconSize: [25, 30],
		iconAnchor:  [0, 20],
		popupAnchor: [1, -34],
		//shadowSize:  [41, 41],
		iconUrl: "{% static 'rom/img/cyan-marker.png' %}",
 		// iconSize: [20, 20],
		// iconAnchor:   [17, 42],
		// popupAnchor: [1, -32],
		// shadowAnchor: [10, 12],
		// shadowSize: [36, 16],
		// bgPos: (geom),
		className: '',
		prefix: '',
		glyph: 'home',
		glyphColor: 'white',
		glyphSize: '10px',	// in CSS units
		glyphAnchor: [0, -5]	// In pixels, counting from the center of the image.
	},

	createIcon: function () {
		var div = document.createElement('div'),
			options = this.options;

		if (options.glyph) {
			div.appendChild(this._createGlyph());
		}

		this._setIconStyles(div, options.className);
		return div;
	},

	_createGlyph: function() {
		var glyphClass,
		    textContent,
		    options = this.options;

		if (!options.prefix) {
			glyphClass = '';
			textContent = options.glyph;
		} else if(options.glyph.slice(0, options.prefix.length+1) === options.prefix + "-") {
			glyphClass = options.glyph;
		} else {
			glyphClass = options.prefix + "-" + options.glyph;
		}

		var span = L.DomUtil.create('span', options.prefix + ' ' + glyphClass);
		span.style.fontSize = options.glyphSize;
		span.style.color = options.glyphColor;
		span.style.width = options.iconSize[0] + 'px';
		span.style.lineHeight = options.iconSize[1] + 'px';
		span.style.textAlign = 'center';
		span.style.marginLeft = options.glyphAnchor[0] + 'px';
		span.style.marginTop = options.glyphAnchor[1] + 'px';
		span.style.pointerEvents = 'none';

		if (textContent) {
			span.innerHTML = textContent;
			span.style.display = 'inline-block';
		}

		return span;
	},

	_setIconStyles: function (div, name) {
		if (name === 'shadow') {
			return L.Icon.prototype._setIconStyles.call(this, div, name);
		}

		var options = this.options,
		    size = L.point(options['iconSize']),
		    anchor = L.point(options.iconAnchor);

		if (!anchor && size) {
			anchor = size.divideBy(2, true);
		}

		div.className = 'leaflet-marker-icon leaflet-glyph-icon ' + name;
		var src = this._getIconUrl('icon');
		if (src) {
			div.style.backgroundImage = "url('" + src + "')";
		}

		if (options.bgPos) {
			div.style.backgroundPosition = (-options.bgPos.x) + 'px ' + (-options.bgPos.y) + 'px';
		}
		if (options.bgSize) {
			div.style.backgroundSize = (options.bgSize.x) + 'px ' + (options.bgSize.y) + 'px';
		}

		if (anchor) {
			div.style.marginLeft = (-anchor.x) + 'px';
			div.style.marginTop  = (-anchor.y) + 'px';
		}

		if (size) {
			div.style.width  = size.x + 'px';
			div.style.height = size.y + 'px';
		}
	}
});

L.icon.glyph = function (options) {
	return new L.Icon.Glyph(options);
};

// Base64-encoded version of glyph-marker-icon.png
 L.Icon.Glyph.prototype.options.iconUrl = 'data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMSAzNy43NiI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNjYzFmNDU7c3Ryb2tlOiNlMTkxOGI7c3Ryb2tlLW1pdGVybGltaXQ6MTA7fTwvc3R5bGU+PC9kZWZzPjx0aXRsZT50YWxsLXJlZC1tYXJrZXI8L3RpdGxlPjxwb2x5Z29uIGNsYXNzPSJjbHMtMSIgcG9pbnRzPSIzMC41IDI1LjUgMTkuNyAyNS41IDE2LjI1IDM2LjI0IDEyLjIgMjUuNSAwLjUgMjUuNSAwLjUgMC41IDMwLjUgMC41IDMwLjUgMjUuNSIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTYuMzUsMTIuNzgiLz48L3N2Zz4=';
