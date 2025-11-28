export function flagFromCountry(country?: string): string {
  if (!country) return "🇪🇺";

  const name = country.trim().toLowerCase();

  const mapping: Record<string, string> = {
    finland: "🇫🇮",
    fi: "🇫🇮",
    suomi: "🇫🇮",

    sweden: "🇸🇪",
    norway: "🇳🇴",
    denmark: "🇩🇰",
    estonia: "🇪🇪",
    latvia: "🇱🇻",
    lithuania: "🇱🇹",
    germany: "🇩🇪",
    poland: "🇵🇱",
    portugal: "🇵🇹",
    spain: "🇪🇸",
    france: "🇫🇷",
    ireland: "🇮🇪",
    netherlands: "🇳🇱",
    belgium: "🇧🇪",
    romania: "🇷🇴",
    hungary: "🇭🇺",
    italy: "🇮🇹",
    bulgaria: "🇧🇬",
    greece: "🇬🇷",
    turkey: "🇹🇷",
    cyprus: "🇨🇾",
    czech: "🇨🇿",
    uk: "🇬🇧",
    "united kingdom": "🇬🇧",
  };

  return mapping[name] ?? "🇪🇺";
}
